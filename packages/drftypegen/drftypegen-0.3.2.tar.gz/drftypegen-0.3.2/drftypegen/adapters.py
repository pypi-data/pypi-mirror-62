import logging

from collections import OrderedDict
from rest_framework.fields import *
from rest_framework import serializers as r_s
from wagtail.core import fields as wg_fields
from django.db import models as dj_model
from django.conf import settings
from django.apps import apps
from pprint import pformat

WAGTAIL_SUPPORT = "wagtail.core" in settings.INSTALLED_APPS

if WAGTAIL_SUPPORT:
    from wagtail.core.models import Page
    from wagtail.core import blocks as wagtail_block
    from wagtail.documents.blocks import DocumentChooserBlock
    from wagtail.images.blocks import ImageChooserBlock
    from wagtail.snippets.blocks import SnippetChooserBlock
    from wagtail.images.api.fields import ImageRenditionField
    from wagtail.contrib.table_block.blocks import TableBlock


logger = logging.getLogger(__name__)

DRF_COMPOSITE_FIELDS = ["ListSerializer", "ManyRelatedField"]

DRF_LIST_FIELDS = ["ListSerializer", "ManyRelatedField", "ListBlock"]

DRF_COMPOSITE_FIELD_RELATION_NAMES = {
    "ListSerializer": "child",
    "ManyRelatedField": "child_relation",
}


DRF_FIELDS = {
    BooleanField: "boolean",
    NullBooleanField: "boolean",
    CharField: "string",
    EmailField: "string",
    RegexField: "string",
    SlugField: "string",
    URLField: "string",
    UUIDField: "string",
    FilePathField: "string",
    IPAddressField: "string",
    IntegerField: "integer",
    FloatField: "number",
    DecimalField: "number",
    DateTimeField: "string",
    DateField: "string",
    TimeField: "string",
    DurationField: "string",
    ChoiceField: "string",
    MultipleChoiceField: "string",
    FileField: "string",
    ImageField: "string",
    ListField: "list",
    DictField: "dict",
    JSONField: "json",
    SerializerMethodField: "json",
    r_s.PrimaryKeyRelatedField: "integer",
    r_s.ManyRelatedField: "list",
}


class BaseAdapter:
    def __init__(self, serializer, suffix=""):
        self.serializer = serializer
        self.instance = serializer()
        self.suffix = suffix

    @classmethod
    def get_all_serializer_data(cls, additional_serializers=[], suffix=""):
        pass

    def transform_field(self, field):
        return {"read_only": False, "write_only": False, "required": True}

    def get_serializer_fields(self, suffix=""):
        return OrderedDict([])

    def get_transformed_data(self):
        fields = self.get_serializer_fields()
        nested = []
        data = OrderedDict([])

        for field in fields.items():

            field_data = self.transform_field(field)
            data[field[0]] = field_data[0]
            nested += field_data[1]
        if hasattr(self.serializer.Meta, "model"):
            name = self.serializer.Meta.model.__name__
        else:
            name = self.serializer.__name__
        nested.append({"name": name + self.suffix, "fields": data})

        return nested


class SerializerAdapter(BaseAdapter):
    def get_serializer_fields(self):
        return self.instance.get_fields()

    @classmethod
    def treverse_urls(cls, root_pattern):
        patterns = []
        for pattern in root_pattern:
            try:
                patterns += cls.treverse_urls(pattern.url_patterns)
            except:
                patterns.append(pattern)
        return patterns

    @staticmethod
    def apiview_filter(view_callback):
        if hasattr(view_callback, "view_class"):
            if hasattr(view_callback.view_class, "serializer_class"):
                return True
        return False

    @classmethod
    def get_all_serializer_data(cls, additional_serializers=[], suffix=""):
        root_urlconf = __import__(settings.ROOT_URLCONF)
        all_urlpatterns = root_urlconf.urls.urlpatterns
        url_patterns = cls.treverse_urls(all_urlpatterns)
        serializers = [
            p.callback.view_class.serializer_class
            for p in url_patterns
            if cls.apiview_filter(p.callback)
        ] + additional_serializers
        data = [
            cls(serializer, suffix).get_transformed_data() for serializer in serializers
        ]
        data = [val for sublist in data for val in sublist]
        return data

    def transform_field(self, field):
        nested = []
        data = {
            "name": field[0],
            "read_only": field[1].read_only,
            "write_only": field[1].write_only,
            "required": field[1].required,
            "nullable": field[1].allow_null,
        }
        field_class = field[1].__class__
        type_data = DRF_FIELDS.get(field_class, None)
        data["openapi_type"] = type_data
        data["type"] = field_class.__name__
        if data["type"] in DRF_COMPOSITE_FIELDS:
            child_class = getattr(
                field[1], DRF_COMPOSITE_FIELD_RELATION_NAMES[data["type"]]
            ).__class__
            if child_class.__name__ == "PrimaryKeyRelatedField":
                data["openapi_type"] = "number"
            else:
                nested_data = SerializerAdapter(
                    child_class, self.suffix
                ).get_transformed_data()
                data["openapi_type"] = nested_data[0]["name"]
                nested.extend(nested_data)
        return data, nested


if WAGTAIL_SUPPORT:

    WAGTAIL_COMPOSITE_FIELDS = ["StreamField"]

    WAGTAIL_BLOCKS_FIELDS = {
        wagtail_block.CharBlock: "string",
        wagtail_block.TextBlock: "string",
        wagtail_block.EmailBlock: "string",
        wagtail_block.IntegerBlock: "integer",
        wagtail_block.FloatBlock: "float",
        wagtail_block.DecimalBlock: "float",
        wagtail_block.RegexBlock: "string",
        wagtail_block.URLBlock: "string",
        wagtail_block.BooleanBlock: "boolean",
        wagtail_block.DateBlock: "string",
        wagtail_block.TimeBlock: "string",
        wagtail_block.DateTimeBlock: "string",
        wagtail_block.RichTextBlock: "string",
        wagtail_block.RawHTMLBlock: "string",
        wagtail_block.BlockQuoteBlock: "string",
        wagtail_block.ChoiceBlock: "string",
        wagtail_block.PageChooserBlock: "integer",
        DocumentChooserBlock: "integer",
        ImageChooserBlock: "integer",
        SnippetChooserBlock: "integer",
        # wagtail_block.EmbedBlock: "string",
        wagtail_block.StaticBlock: "string",
        wagtail_block.ListBlock: "composite_block",
        wagtail_block.StructBlock: "composite_block",
        wagtail_block.StreamBlock: "composite_block",
        TableBlock: "json",
    }
    WAGTAIL_COMPOSITE_BLOCKS = [
        "StructBlock",
        "ListBlock",
        "StreamBlock",
        "StreamField",
        "TableBlock",
    ]

    WAGTAIL_COMPOSITE_BLOCK_CLASSES = [
        wagtail_block.ListBlock,
        wagtail_block.StructBlock,
        wagtail_block.StreamBlock,
    ]

    WAGTAIL_FIELDS = {
        dj_model.CharField: "string",
        dj_model.BigIntegerField: "integer",
        dj_model.DateField: "string",
        dj_model.BooleanField: "boolean",
        dj_model.DateTimeField: "string",
        dj_model.DecimalField: "float",
        dj_model.EmailField: "string",
        dj_model.FileField: "string",
        dj_model.FloatField: "float",
        dj_model.ImageField: "string",
        dj_model.IntegerField: "integer",
        dj_model.PositiveSmallIntegerField: "integer",
        dj_model.GenericIPAddressField: "string",
        dj_model.PositiveIntegerField: "integer",
        dj_model.SlugField: "string",
        dj_model.SmallIntegerField: "integer",
        dj_model.TextField: "string",
        dj_model.URLField: "string",
        dj_model.UUIDField: "string",
        dj_model.ForeignKey: "integer",
        dj_model.OneToOneField: "integer",
        dj_model.ManyToManyField: "list",
        wg_fields.RichTextField: "string",
        wg_fields.StreamField: "child",
    }

    IMAGE_RENDITION_FIELD_SPEC = {
        "name": "ImageRenditionField",
        "fields": [
            {
                "name": "height",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "integer",
                "type": "IntegerBlock",
            },
            {
                "name": "width",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "integer",
                "type": "IntegerBlock",
            },
            {
                "name": "url",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharBlock",
            },
        ],
    }

    PAGE_PARENT_META_FIELD_DATA = {
        "name": "PageParentMeta",
        "fields": [
            {
                "name": "type",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "detail_url",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "html_url",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
        ],
    }

    META_PARENT = {
        "name": "PageParent",
        "fields": [
            {
                "name": "id",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "integer",
                "type": "IntegerField",
            },
            {
                "name": "meta",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "PageParentMeta",
                "type": "PageParentMeta",
            },
            {
                "name": "title",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
        ],
    }

    META_FIELD_DATA = {
        "name": "Meta",
        "fields": [
            {
                "name": "type",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "detail_url",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "html_url",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "slug",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "first_published_at",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "show_in_menus",
                "read_only": True,
                "write_only": False,
                "required": False,
                "nullable": False,
                "openapi_type": "boolean",
                "type": "BooleanField",
            },
            {
                "name": "seo_title",
                "read_only": True,
                "write_only": False,
                "required": False,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "search_description",
                "read_only": True,
                "write_only": False,
                "required": False,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            },
            {
                "name": "parent",
                "read_only": True,
                "write_only": False,
                "required": False,
                "nullable": True,
                "openapi_type": "Meta",
                "type": "Meta",
            },
        ],
    }

    class WagtailAdapter(SerializerAdapter):
        def __init__(self, wagtail_model, suffix=""):
            self.wagtail_model = wagtail_model
            self.image_rendition_added = False
            self.suffix = suffix

        @classmethod
        def get_all_serializer_data(cls, additional_serializers=[], suffix=""):
            models = apps.get_models()
            rel_m = [m for m in models if issubclass(m, Page) and m != Page]
            transformed_data = []

            for m in rel_m:
                data = cls(m, suffix).get_transformed_data()

                if data is not None:

                    transformed_data.extend(data)

            transformed_data = [
                PAGE_PARENT_META_FIELD_DATA,
                META_PARENT,
                META_FIELD_DATA,
            ] + transformed_data

            return_data = OrderedDict([])
            for td in transformed_data:
                return_data[td["name"]] = td

            return list(return_data.values())

        def get_all_fields(self):
            return getattr(self.wagtail_model, "api_fields", [])

        def get_transformed_data(self):
            fields = self.get_all_fields()
            if not fields:
                return None
            data = OrderedDict([])
            nested = []

            data["id"] = {
                "name": "id",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "integer",
                "type": "IntegerField",
            }
            data["title"] = {
                "name": "title",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "string",
                "type": "CharField",
            }
            data["meta"] = {
                "name": "meta",
                "read_only": True,
                "write_only": False,
                "required": True,
                "nullable": False,
                "openapi_type": "Meta",
                "type": "Meta",
            }

            for field in fields:
                f = getattr(field, "serializer", False)
                if not f:
                    try:
                        deref_field = getattr(self.wagtail_model, field.name)
                        f = deref_field.field
                        field_data = self.transform_field((field.name, f))
                        data[field.name] = field_data[0]

                        nested += field_data[1]

                    except Exception as e:
                        data[field.name] = {
                            "name": field.name,
                            "read_only": True,
                            "write_only": False,
                            "required": False,
                            "nullable": True,
                            "openapi_type": "any",
                            "type": "MethodField",
                        }
                else:
                    if f.__class__.__name__ == "ImageRenditionField":
                        data[field.name] = {
                            "name": field.name,
                            "read_only": True,
                            "write_only": False,
                            "required": False,
                            "nullable": True,
                            "openapi_type": "ImageRenditionField",
                            "type": "ImageRenditionField",
                        }

                        if not self.image_rendition_added:
                            nested.append(IMAGE_RENDITION_FIELD_SPEC)

            nested.append(
                {
                    "name": self.wagtail_model.__name__ + self.suffix,
                    "fields": data,
                    "stream": self.wagtail_model.__name__ == "StreamField",
                }
            )

            return nested

        def transform_stream_field(self, field, name=None):
            """Takes only stream field one block field"""

            is_nullable = True if field.required else False

            field_class = field.__class__

            field_class_name = field_class.__name__

            data = {
                "name": name,
                "read_only": True,
                "write_only": False,
                "required": field.required,
                "nullable": is_nullable,
            }
            type_data = WAGTAIL_BLOCKS_FIELDS.get(field_class, None)
            if type_data is None:
                for key, val in WAGTAIL_BLOCKS_FIELDS.items():
                    if issubclass(field_class, key):
                        type_data = val
                        break
            data["openapi_type"] = type_data
            data["type"] = field_class.__name__
            return data

        def stream_field_parser(self, block):
            """parse streamfield and pass block field to transform_stream_field function"""

            name = block[0]
            block_data = block[1]
            # stream_data = []
            additional_blocks = []
            get_stream_data = self.transform_stream_field(block_data, name)

            child_name = get_stream_data["type"]

            if child_name in ["StreamBlock", "StructBlock"]:
                child_name = name.capitalize() + self.suffix

            if issubclass(block_data.__class__, wagtail_block.StreamBlock):

                child_data = {
                    "name": child_name + self.suffix,
                    "fields": [],
                    "stream": True,
                }
                childs = block_data.child_blocks
                for item in childs.items():

                    get_nested_stream_data = self.stream_field_parser(item)

                    additional_blocks += get_nested_stream_data[1]
                    child_data["fields"].append(get_nested_stream_data[0])

                additional_blocks.append(child_data)
                get_stream_data["type"] = child_data["name"]

            elif issubclass(block_data.__class__, wagtail_block.StructBlock):
                child_data = {"name": child_name + self.suffix, "fields": []}
                childs = block_data.child_blocks
                for item in childs.items():

                    get_nested_stream_data = self.stream_field_parser(item)

                    additional_blocks += get_nested_stream_data[1]
                    child_data["fields"].append(get_nested_stream_data[0])

                additional_blocks.append(child_data)
                get_stream_data["openapi_type"] = child_name + self.suffix

            elif issubclass(block_data.__class__, wagtail_block.ListBlock):
                get_nested_stream_data = self.stream_field_parser(
                    (name + "_child", block_data.child_block)
                )
                if len(get_nested_stream_data[1]) == 1:
                    child_name = (
                        f"{''.join(x.capitalize() or '_' for x in name.split('_'))}Child"
                        + self.suffix
                    )
                    get_nested_stream_data[1][0]["name"] = child_name
                    additional_blocks += get_nested_stream_data[1]
                    get_stream_data["openapi_type"] = child_name
                else:
                    get_stream_data["openapi_type"] = get_nested_stream_data[0][
                        "openapi_type"
                    ]
                # stream_data += get_nested_stream_data
            else:
                name = block[0]
                block_data = block[1]

            # stream_data.append(get_stream_data)
            return get_stream_data, additional_blocks

        # def parse_stream_list_block(self, list_block):

        def stream_field_decompose(self, stream_field):
            """takes entire streamfield and decompose and pass block to stream_field_parser function"""

            block_list = [
                block for block in stream_field.stream_block.child_blocks.items()
            ]
            stream = []
            models = []
            types = set([])

            for block in block_list:
                stream_block = self.stream_field_parser(block)

                types.add(stream_block[0]["openapi_type"])
                stream.append(stream_block[0])
                models.extend(stream_block[1])

            types = sorted(list(types))

            return stream, types, models

        def transform_field(self, field_data):
            field = field_data[1]
            # if issubclass(field.__class__, Field):
            #     return super().transform_field(field_data)
            is_required = False if field.blank else True
            other_models = []
            data = {
                "name": field_data[0],
                "read_only": True,
                "write_only": False,
                "required": is_required,
                "nullable": field.null,
            }
            field_class = field.__class__
            type_data = WAGTAIL_FIELDS.get(field_class, None)
            data["openapi_type"] = type_data
            data["type"] = field_class.__name__

            if data["type"] in WAGTAIL_COMPOSITE_FIELDS:
                stream, types, models = self.stream_field_decompose(field)
                for child_block in models:
                    other_models.append(child_block)

                # other_models.append(streams[0][0])
                data["openapi_type"] = types
            total = f"Total: {len(other_models) + 1}"
            # return streams
            return data, other_models
