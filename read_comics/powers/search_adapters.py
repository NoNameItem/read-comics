from django.utils.html import strip_tags
from watson import search as watson


class PowerSearchAdapter(watson.SearchAdapter):
    def get_title(self, obj):
        if obj.aliases:
            return obj.name + "\n" + obj.aliases
        else:
            return obj.name

    def get_short_description(self, obj):
        if obj.html_description:
            return strip_tags(obj.html_description)
        else:
            return ''

    def get_description(self, obj):
        return ''
