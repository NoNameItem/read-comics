# Docs: [[docs/backend/locations/search_adapters.md]]
from search.search_adapters import BaseSearchAdapter


class LocationSearchAdapter(BaseSearchAdapter):
    SECTION = "Location"
    ICON = "fa-map-marker-alt"
