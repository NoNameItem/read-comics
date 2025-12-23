# Locations

Stores geographic and fictional locations appearing in comic issues, with ComicVine syncing and counting capabilities.

## Documentation

### Core Models
- [`models.md`](models.md) — Location with first issue tracking and watchable status

### API Layer
- [`api/endpoints.md`](api/endpoints.md) — REST endpoint specifications
- [`api/serializers.md`](api/serializers.md) — LocationsListSerializer, LocationDetailSerializer, ConceptTechnicalInfoSerializer
- [`api/viewsets.md`](api/viewsets.md) — LocationViewSet with aggregated counts and issue filtering

### Search & Tasks
- [`search_adapters.md`](search_adapters.md) — Full-text search integration
- [`tasks.md`](tasks.md) — ComicVine API syncing and Scrapy spiders

## Key Features
- **ComicVine Integration** — Automatic field mapping and periodic sync
- **First Appearance Tracking** — Links to initial issue appearance
- **Related Content Counting** — Aggregated issue and volume counts
- **Watchable Items** — Users can watch locations for missing issues
- **Aliases Support** — Multiple names per location
- **Full-Text Search** — Quick location lookup by name or description
