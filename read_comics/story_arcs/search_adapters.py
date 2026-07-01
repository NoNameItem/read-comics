# Docs: [[docs/backend/story_arcs/search_adapters.md]]
from search.search_adapters import BaseSearchAdapter


class StoryArcSearchAdapter(BaseSearchAdapter):
    SECTION = "Story Arc"
    ICON = "fa-books"
