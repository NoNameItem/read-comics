# Issues API

REST API for accessing comic issues with filtering, sorting, and user progress tracking.

## Documentation

- [`endpoints.md`](endpoints.md) — REST endpoint specifications and examples
- [`serializers.md`](serializers.md) — Response serializer schemas
- [`viewsets.md`](viewsets.md) — ViewSet configuration and behavior

## Key Features

- **List Endpoint** — Browse issues with pagination and optional `?hide-finished=yes|no`
- **Detail Endpoint** — Full issue data with navigation (previous/next issue slugs)
- **Smart Pagination** — Unique ordering for consistent navigation across page changes
- **User Tracking** — `is_finished` flag shows completion status (authenticated users only)
- **Multiple Serializers** — Compact list, full detail, and admin tech-info views
- **Meta Actions** — `/count/` for total count, `/tech-info/` for ComicVine sync status
