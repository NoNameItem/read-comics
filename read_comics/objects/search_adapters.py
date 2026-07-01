# Docs: [[docs/backend/objects/search_adapters.md]]
from search.search_adapters import BaseSearchAdapter


class ObjectSearchAdapter(BaseSearchAdapter):
    SECTION = "Object"
    ICON = "fa-swords"
