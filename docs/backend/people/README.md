# People

Stores data about creators, artists, and industry contributors with ComicVine syncing and counting capabilities.

## Documentation

### Core Models
- [`models.md`](models.md) — Person model with biographical data and watchable status

### API Layer
- [`api/endpoints.md`](api/endpoints.md) — REST endpoint specifications
- [`api/serializers.md`](api/serializers.md) — PeopleListSerializer
- [`api/viewsets.md`](api/viewsets.md) — PeopleViewSet with aggregated counts and issue filtering

### Search & Tasks
- [`search_adapters.md`](search_adapters.md) — Full-text search integration
- [`tasks.md`](tasks.md) — ComicVine API syncing and Scrapy spiders

## Key Features
- **ComicVine Integration** — Automatic field mapping and periodic sync
- **Biographical Data** — Name, aliases, birth/death dates, hometown/country
- **Related Content Counting** — Aggregated issue and volume counts
- **Watchable Items** — Users can watch people for missing issues
- **Full-Text Search** — Quick creator lookup by name or description
- **List-Only API** — Efficient browsing without detail endpoint
