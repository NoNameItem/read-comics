# Objects

Stores items, artifacts, and equipment appearing in comic issues, with ComicVine syncing and counting capabilities.

## Documentation

### Core Models
- [`models.md`](models.md) — Object with first appearance tracking and watchable status

### API Layer
- [`api/endpoints.md`](api/endpoints.md) — REST endpoint specifications
- [`api/serializers.md`](api/serializers.md) — ObjectsListSerializer
- [`api/viewsets.md`](api/viewsets.md) — ObjectViewSet with aggregated counts and issue filtering

### Search & Tasks
- [`search_adapters.md`](search_adapters.md) — Full-text search integration
- [`tasks.md`](tasks.md) — ComicVine API syncing and Scrapy spiders

## Key Features
- **ComicVine Integration** — Automatic field mapping and periodic sync
- **First Appearance Tracking** — Links to initial issue appearance
- **Related Content Counting** — Aggregated issue and volume counts
- **Watchable Items** — Users can watch objects for missing issues
- **Aliases Support** — Multiple names per object
- **Full-Text Search** — Quick object lookup by name or description
- **List-Only API** — Efficient browsing without detail endpoint
