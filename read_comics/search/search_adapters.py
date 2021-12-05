from watson.search import SearchAdapter


class BaseSearchAdapter(SearchAdapter):
    SECTION = None
    ICON = None

    def get_title(self, obj):
        if hasattr(obj, 'aliases') and obj.aliases:
            return obj.name + "\n" + obj.aliases
        else:
            return obj.name

    def get_description(self, obj):
        if hasattr(obj, 'short_description') and obj.short_description:
            return obj.short_description
        else:
            return ''

    def get_content(self, obj):
        return ''

    def get_meta(self, obj):
        meta = super(BaseSearchAdapter, self).get_meta(obj)
        meta['section'] = self.SECTION
        meta['search_display'] = str(obj)
        meta['icon'] = self.ICON
        meta['img_url'] = obj.square_tiny
        return meta
