# Docs: [[docs/backend/concepts/search_adapters.md]]
from search.search_adapters import BaseSearchAdapter


class ConceptSearchAdapter(BaseSearchAdapter):
    SECTION = "Concept"
    ICON = "fa-brain"
