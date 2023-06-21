from typing import OrderedDict

from django.forms import ImageField as DjangoImageField
from rest_framework.fields import Field, flatten_choices_dict, to_choices_dict
from rest_framework.settings import api_settings
from utils.fields import ThumbnailImageFieldFile


class ThumbnailImageField(Field):
    default_error_messages = {
        "invalid_image": "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
    }

    def __init__(self, *args, **kwargs) -> None:
        self._django_image_field = kwargs.pop("_DjangoImageField", DjangoImageField)
        self.max_length = kwargs.pop("max_length", None)
        self.allow_empty_file = kwargs.pop("allow_empty_file", False)
        if "use_url" in kwargs:
            self.use_url = kwargs.pop("use_url")
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        file_name = None
        file_size = None
        try:
            # `UploadedFile` objects should have name and size attributes.
            file_name = data.name
            file_size = data.size
        except AttributeError:
            self.fail("invalid")

        if not file_name:
            self.fail("no_name")
        if not self.allow_empty_file and not file_size:
            self.fail("empty")
        if self.max_length and len(file_name) > self.max_length:
            self.fail("max_length", max_length=self.max_length, length=len(file_name))

        file_object = data

        django_field = self._django_image_field()
        django_field.error_messages = self.error_messages
        return django_field.clean(file_object)

    def to_representation(self, value: ThumbnailImageFieldFile) -> dict[str, str] | None:
        if not value:
            return None

        use_url = getattr(self, "use_url", api_settings.UPLOADED_FILES_USE_URL)
        if use_url:
            try:
                url = value.url
                thumb_url = value.thumb_url
            except AttributeError:
                return None
            request = self.context.get("request", None)
            if request is not None:
                return {"image": request.build_absolute_uri(url), "thumbnail": request.build_absolute_uri(thumb_url)}
            return {"image": url, "thumbnail": thumb_url}

        return {"image": value.name, "thumbnail": value.thumb_name}


class NestedChoiceField(Field):
    default_error_messages = {"invalid_choice": '"{input}" is not a valid choice.'}
    html_cutoff = None
    html_cutoff_text = "More than {count} items..."

    def __init__(self, choices, **kwargs) -> None:
        self.choices = choices
        self.html_cutoff = kwargs.pop("html_cutoff", self.html_cutoff)
        self.html_cutoff_text = kwargs.pop("html_cutoff_text", self.html_cutoff_text)

        self.allow_blank = kwargs.pop("allow_blank", False)

        super().__init__(**kwargs)

    def _get_choices(self) -> OrderedDict:
        return self._choices

    def _set_choices(self, choices) -> None:
        self.grouped_choices = to_choices_dict(choices)  # pylint: disable=locally-disabled, W0201
        self._choices = flatten_choices_dict(self.grouped_choices)  # pylint: disable=locally-disabled, W0201

        # Map the string representation of choices to the underlying value.
        # Allows us to deal with eg. integer choices while supporting either
        # integer or string input, but still get the correct datatype out.
        self.choice_strings_to_values = {  # pylint: disable=locally-disabled, W0201
            str(key): key for key in self.choices
        }
        self.choice_strings_to_labels = {  # pylint: disable=locally-disabled, W0201  # noqa
            str(key): label for key, label in self.choices.items()
        }

    choices = property(_get_choices, _set_choices)

    def to_internal_value(self, data: str | int | tuple[str | int, str | int | tuple]) -> str:
        if data == "" and self.allow_blank:
            return ""
        try:
            if isinstance(data, dict):
                data = data["value"]
            return self.choice_strings_to_values[str(data)]
        except KeyError:
            self.fail("invalid_choice", input=data)
            return ""

    def to_representation(self, value: str) -> dict | str | None:
        if value in ("", None):
            return value
        return {
            "value": self.choice_strings_to_values.get(str(value), value),
            "label": self.choice_strings_to_labels.get(str(value), ""),
        }
