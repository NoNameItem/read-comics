from search.search_adapters import BaseSearchAdapter


class IssueSearchAdapter(BaseSearchAdapter):
    SECTION = "Issue"
    ICON = "fa-book-open"

    def get_title(self, obj):
        return obj.get_full_name()
