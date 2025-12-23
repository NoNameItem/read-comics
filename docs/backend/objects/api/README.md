# Objects API

REST API for accessing comic objects/artifacts with aggregated counts and first appearance information.

## Documentation

- [`endpoints.md`](endpoints.md) — REST endpoint specifications and examples
- [`serializers.md`](serializers.md) — Response serializer schemas
- [`viewsets.md`](viewsets.md) — ViewSet configuration and behavior

## Key Features

- **List Endpoint** — Browse objects alphabetically with issue/volume counts
- **No Detail Endpoint** — Objects only expose list view via API (retrieve not available)
- **Counting** — Aggregated issues and volumes featuring each object
- **Filtering** — Only includes objects with at least one related issue
- **Single Serializer** — ObjectsListSerializer for consistent list response
- **Meta Actions** — `/count/` for total count
