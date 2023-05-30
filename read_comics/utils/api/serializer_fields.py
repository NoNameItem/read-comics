from typing import OrderedDict

from rest_framework import serializers
from rest_framework.fields import ChoiceField, flatten_choices_dict, to_choices_dict
from rest_framework.settings import api_settings
from utils.fields import ThumbnailImageFieldFile


class ThumbnailImageField(serializers.ImageField):
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


class NestedChoiceField(ChoiceField):
    def _get_choices(self) -> OrderedDict:
        return self._choices

    def _set_choices(self, choices) -> None:
        self.grouped_choices = to_choices_dict(choices)
        self._choices = flatten_choices_dict(self.grouped_choices)

        # Map the string representation of choices to the underlying value.
        # Allows us to deal with eg. integer choices while supporting either
        # integer or string input, but still get the correct datatype out.
        self.choice_strings_to_values = {str(key): key for key in self.choices}
        self.choice_strings_to_labels = {str(key): label for key, label in self.choices.items()}

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

    def to_representation(self, value: str) -> dict | str | None:
        if value in ("", None):
            return value
        return {
            "value": self.choice_strings_to_values.get(str(value), value),
            "label": self.choice_strings_to_labels.get(str(value), ""),
        }
