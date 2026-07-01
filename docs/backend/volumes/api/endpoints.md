# Volumes API endpoints

All endpoints are powered by [`VolumesViewSet`](viewsets.md#volumesviewset). The viewset is read-only and exposes standard list/detail operations plus custom `count` and `started` actions.

## List: `GET /api/volumes/`

Returns a paginated list of comic book volumes with publisher metadata and reading progress annotations. Supports filtering by finished status and issue count.

- **ViewSet**: [`VolumesViewSet`](viewsets.md#volumesviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`VolumesListSerializer`](serializers.md#volumeslistserializer)
- **Query params**:
  - `ordering` (`start_year`, `name`, `issues_count`). Defaults to `start_year`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `hide-finished=yes` filters out volumes where the user has read every issue.
  - `show-all=yes` removes the implicit `issues_count > 0` filter.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "amazing-spider-man",
    "image": "https://.../asm.jpg",
    "publisher": {"name": "Marvel", "image": "https://...", "slug": "marvel"},
    "name": "The Amazing Spider-Man",
    "short_description": "Peter Parker's flagship run.",
    "issues_count": 900,
    "finished_count": 250,
    "is_finished": false,
    "start_year": 1963
  }
  ```

## Detail: `GET /api/volumes/{slug}/`

Retrieves detailed information about a specific volume. Currently returns the same fields as the list endpoint.

- **ViewSet**: [`VolumesViewSet`](viewsets.md#volumesviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`VolumesListSerializer`](serializers.md#volumeslistserializer)
- **Path parameter**: `{slug}` (the slug field of the Volume model).
- **Response fields**: Same as list endpoint above.

## Count: `GET /api/volumes/count/`

Returns the total count of volumes after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`VolumesViewSet`](viewsets.md#volumesviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (`hide-finished`, `show-all`).
- **Response**:
  ```json
  {
    "count": 456
  }
  ```

## Started: `GET /api/volumes/started/`

Returns volumes that have been started but not finished by the authenticated user, sorted by most recently read issue.

- **ViewSet**: [`VolumesViewSet`](viewsets.md#volumesviewset)
- **Action**: `started` (from `StartedActionMixin`)
- **Serializer**: [`StartedVolumeSerializer`](serializers.md#startedvolumeserializer)
- **Permissions**: Authenticated users only.
- **Query params**: Standard pagination parameters.
- **Response structure**: Returns volumes with `is_started=True` and `is_finished=False`, sorted by `-max_finished_date`. Each entry contains:
  ```json
  {
    "slug": "sandman",
    "display_name": "Sandman",
    "image": "https://.../sandman.jpg",
    "max_finished_date": "2025-12-01T12:00:00Z",
    "finished_count": 5,
    "issues_count": 75
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/volumes/<slug>/` (detail serializer slug lookup currently PK; map marks as `NEEDS WORK`).
- `GET /api/volumes/<slug>/technical-info/`
- `GET /api/volumes/random/`
- `GET /api/volumes/<slug>/start-watch/`
- `GET /api/volumes/<slug>/stop-watch/`
- `GET /api/volumes/<slug>/mark-finished/`
- `GET /api/volumes/<slug>/issues/`
- `GET /api/volumes/<slug>/characters/`
- `GET /api/volumes/<slug>/died/`
- `GET /api/volumes/<slug>/concepts/`
- `GET /api/volumes/<slug>/locations/`
- `GET /api/volumes/<slug>/objects/`
- `GET /api/volumes/<slug>/authors/`
- `GET /api/volumes/<slug>/story-arcs/`
- `GET /api/volumes/<slug>/teams/`
- `GET /api/volumes/<slug>/disbanded/`
- `GET /api/volumes/<slug>/first-appearances/`
- `GET /api/volumes/<slug>/issues/{issue_slug}/`

All listed endpoints are flagged as `PLAN` in `DRF_MIGRATION_URL_MAP.md` (with the detail view marked `NEEDS WORK`) and are pending slug-aware serializers/actions.