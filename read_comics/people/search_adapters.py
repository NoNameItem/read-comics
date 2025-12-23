# Docs: [[docs/backend/people/search_adapters.md]]
from search.search_adapters import BaseSearchAdapter


class PersonSearchAdapter(BaseSearchAdapter):
    SECTION = "Person"
    ICON = "fa-people-carry"
