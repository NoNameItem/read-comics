# Publishers API endpoints

All endpoints are powered by [`PublishersViewSet`](viewsets.md#publishersviewset). The viewset is read-only and exposes standard list/detail operations plus a custom `count` action.

## List: `GET /api/publishers/`

Returns a paginated list of comic book publishers with compact metadata. Filters out publishers without matched issues by default; use `?show-all=yes` to include all records. Uses `issues_lookup = "volumes__issues"` so counters aggregate all volumes under the publisher.

- **ViewSet**: [`PublishersViewSet`](viewsets.md#publishersviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`PublishersListSerializer`](serializers.md#publisherslistserializer)
- **Query params**:
  - `ordering` (`name`, `issues_count`, `volumes_count`). Defaults to `name`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `show-all=yes` returns publishers even if no matched issues; default is `no`, which applies `OnlyWithIssuesQuerySetMixin` filter.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "marvel",
    "image": "https://.../marvel.jpg",
    "name": "Marvel",
    "short_description": "Publisher of many IPs.",
    "issues_count": 5000,
    "volumes_count": 300
  }
  ```

## Detail: `GET /api/publishers/{slug}/`

Retrieves information about a specific publisher. Currently returns the same fields as the list endpoint.

- **ViewSet**: [`PublishersViewSet`](viewsets.md#publishersviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`PublishersListSerializer`](serializers.md#publisherslistserializer)
- **Path parameter**: `{slug}` (the slug field of the Publisher model).
- **Response fields**: Same as list endpoint above.

## Count: `GET /api/publishers/count/`

Returns the total count of publishers after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`PublishersViewSet`](viewsets.md#publishersviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (applies `OnlyWithIssuesQuerySetMixin` unless `?show-all=yes`).
- **Response**:
  ```json
  {
    "count": 25
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/publishers/{slug}/` – slug detail view expected once serializers map under-the-hood PKs to slugs (`NEEDS WORK` entry).
- `GET /api/publishers/{slug}/technical-info/` – expose ComicVine audit fields for the publisher.
- `GET /api/publishers/{slug}/start-watch/` – add the publisher to the user's tracked list.
- `GET /api/publishers/{slug}/stop-watch/` – remove the publisher from tracking.
- `GET /api/publishers/{slug}/issues/` – list issues published by the publisher.
- `GET /api/publishers/{slug}/characters/` – list characters tied to the publisher.
- `GET /api/publishers/{slug}/teams/` – list teams under the publisher.
- `GET /api/publishers/{slug}/story-arcs/` – list story arcs belonging to the publisher.
- `GET /api/publishers/{slug}/volumes/` – list volumes published by the publisher.
- `GET /api/publishers/{slug}/issues/{issue_slug}/` – issue-level detail scoped to the publisher.

Each route is `PLAN` in `DRF_MIGRATION_URL_MAP.md` until slug lookups and supporting serializers are in place.