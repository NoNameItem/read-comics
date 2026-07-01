# People API

REST API for accessing creator/contributor data with aggregated issue and volume counts.

## Documentation

- [`endpoints.md`](endpoints.md) — REST endpoint specifications and examples
- [`serializers.md`](serializers.md) — Response serializer schemas
- [`viewsets.md`](viewsets.md) — ViewSet configuration and behavior

## Key Features

- **List Endpoint** — Browse creators alphabetically with issue/volume counts
- **No Detail Endpoint** — People only expose list view via API (retrieve not available)
- **Counting** — Aggregated issues and volumes featuring each creator
- **Filtering** — Only includes persons with at least one related issue
- **Single Serializer** — PeopleListSerializer for consistent list response
- **Meta Actions** — `/count/` for total count