# Docs: [[docs/backend/teams/search_adapters.md]]
from search.search_adapters import BaseSearchAdapter


class TeamSearchAdapter(BaseSearchAdapter):
    SECTION = "Team"
    ICON = "fa-users"
