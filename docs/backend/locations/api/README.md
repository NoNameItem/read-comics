# Locations API

REST API for accessing comic locations with aggregated counts and first appearance information.

## Documentation

- [`endpoints.md`](endpoints.md) — REST endpoint specifications and examples
- [`serializers.md`](serializers.md) — Response serializer schemas
- [`viewsets.md`](viewsets.md) — ViewSet configuration and behavior

## Key Features

- **List Endpoint** — Browse locations alphabetically with issue/volume counts
- **Detail Endpoint** — Full location data with first appearance reference
- **Counting** — Aggregated issues and volumes featuring each location
- **Filtering** — Only includes locations with at least one related issue
- **Multiple Serializers** — Compact list, full detail, and admin tech-info views
- **Meta Actions** — `/count/` for total count, `/tech-info/` for ComicVine sync status
