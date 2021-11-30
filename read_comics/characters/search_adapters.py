from django.utils.html import strip_tags
from watson import search as watson


class CharacterSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        title = obj.name
        if obj.aliases:
            title += "\n" + obj.aliases
        if obj.real_name:
            title += "\n" + obj.real_name
        return title or ''

    def get_description(self, obj):
        if obj.short_description:
            return obj.short_description
        return ''

    def get_content(self, obj):
        if obj.html_description:
            return strip_tags(obj.html_description)
        return ''
