# Docs: [[docs/backend/characters/search_adapters.md]]
from read_comics.search.search_adapters import BaseSearchAdapter


class CharacterSearchAdapter(BaseSearchAdapter):
    SECTION = "Character"
    ICON = "fa-bat"
