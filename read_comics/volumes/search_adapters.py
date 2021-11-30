from django.utils.html import strip_tags
from watson import search as watson


class VolumeSearchAdapter(watson.SearchAdapter):
    def get_title(self, obj):
        title = obj.name
        if obj.start_year:
            title += "\n" + str(obj.start_year)
        if obj.aliases:
            title += "\n" + obj.aliases

        return title or ''

    def get_description(self, obj):
        if obj.short_description:
            return obj.short_description
        else:
            return ''

    def get_content(self, obj):
        if obj.html_description:
            return strip_tags(obj.html_description)
        else:
            return ''
