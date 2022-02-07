from search.search_adapters import BaseSearchAdapter


class VolumeSearchAdapter(BaseSearchAdapter):
    SECTION = 'Volume'
    ICON = 'fa-book-spells'

    def get_title(self, obj):
        return str(obj.name) + ' ' + str(obj.start_year) + "\n" + str(obj.aliases)
