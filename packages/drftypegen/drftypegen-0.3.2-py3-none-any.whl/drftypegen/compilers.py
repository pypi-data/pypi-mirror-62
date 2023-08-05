import logging
from django.conf import settings
from .adapters import *

from pprint import pformat

logger = logging.getLogger(__name__)


class BaseCompiler:
    adapter_class = None

    def generate_field(self, data):
        return "Not Implemented"

    def generate_serializer_body(self, serializer_data):
        return "Not Implemented"

    def generate(self, additional_serializers=[]):
        return "Not Implemented"


TS_TYPE_MAP = {
    "integer": "number",
    "float": "number",
    "decimal": "string",
    "json": "any",
}


class TypeScriptCompiler(BaseCompiler):
    def __init__(self, adapter_class=SerializerAdapter, suffix=""):
        self.adapter_class = adapter_class
        self.suffix = suffix

    @staticmethod
    def type_resolver(field):
        ftype = field["openapi_type"]
        if ftype == "composite_block":
            return field["type"]
        return TS_TYPE_MAP.get(ftype, ftype)

    def generate_field(self, data):
        # logger.critical(data["type"])
        if data["type"] in DRF_LIST_FIELDS:
            dtype = f"Array<{self.type_resolver(data)}>"
        elif data["type"] == "StreamField":
            # logger.critical(data)
            dtype = f"Array<{' | '.join(sorted([TS_TYPE_MAP.get(d, d) for d in data['openapi_type']]))}>"

        else:
            dtype = self.type_resolver(data)

        if data["nullable"]:
            dtype = f"{dtype} | null"
        return f"\t{'readonly ' if data['read_only'] else ''}{data['name']}{'?' if not data['required'] else ''}: {dtype};"

    def generate_serializer_body(self, serializer_data):
        if serializer_data.get("stream", False):
            # logger.critical(serializer_data)
            type = " | ".join(
                [
                    TS_TYPE_MAP.get(d["openapi_type"], d["openapi_type"])
                    for d in serializer_data["fields"]
                ]
            )
            return f"type {serializer_data['name']} = {type};"
        else:
            try:
                values = serializer_data["fields"].values()
            except:
                values = serializer_data["fields"]
            return "\n".join(
                [
                    f"export interface {serializer_data['name']} {{",
                    *[self.generate_field(field) for field in values],
                    "}",
                ]
            )

    def generate(self, additional_serializers=[]):
        data = self.adapter_class.get_all_serializer_data(
            additional_serializers, self.suffix
        )
        # logger.critical(pformat(data))
        interface = [self.generate_serializer_body(sbody) for sbody in data]
        return "\n\n".join(interface)
