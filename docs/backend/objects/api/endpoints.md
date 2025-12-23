# Objects API endpoints

All endpoints are powered by [`ObjectViewSet`](viewsets.md#objectviewset). The viewset is read-only and exposes standard list/detail operations plus a custom `count` action.

## List: `GET /api/objects/`

Returns a paginated list of comic book objects with compact metadata. Filters out objects without matched issues by default; use `?show-all=yes` to include all records.

- **ViewSet**: [`ObjectViewSet`](viewsets.md#objectviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`ObjectsListSerializer`](serializers.md#objectslistserializer)
- **Query params**:
  - `ordering` (`name`, `issues_count`, `volumes_count`). Defaults to `name`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `show-all=yes` returns objects even if no matched issues; default is `no`, which applies `OnlyWithIssuesQuerySetMixin` filter.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "infinity-gauntlet",
    "image": "https://.../gauntlet.jpg",
    "name": "Infinity Gauntlet",
    "short_description": "The universe-level artifact.",
    "issues_count": 12,
    "volumes_count": 3
  }
  ```

## Detail: `GET /api/objects/{slug}/`

Retrieves information about a specific object. Currently returns the same fields as the list endpoint.

- **ViewSet**: [`ObjectViewSet`](viewsets.md#objectviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`ObjectsListSerializer`](serializers.md#objectslistserializer)
- **Path parameter**: `{slug}` (the slug field of the Object model).
- **Response fields**: Same as list endpoint above.

## Count: `GET /api/objects/count/`

Returns the total count of objects after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`ObjectViewSet`](viewsets.md#objectviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (applies `OnlyWithIssuesQuerySetMixin` unless `?show-all=yes`).
- **Response**:
  ```json
  {
    "count": 42
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/objects/{slug}/` – replace the Django detail view once slug-based serializers are ready (`NEEDS WORK` in the map).
- `GET /api/objects/{slug}/technical-info/` – expose the object's ComicVine metadata.
- `GET /api/objects/{slug}/start-watch/` – start tracking an object.
- `GET /api/objects/{slug}/stop-watch/` – stop tracking the object.
- `GET /api/objects/{slug}/issues/` – list issues featuring the object.
- `GET /api/objects/{slug}/volumes/` – list volumes containing the object.
- `GET /api/objects/{slug}/issues/{issue_slug}/` – get a specific issue slug for the object.

Each line is currently `PLAN` (with the detail view flagged as `NEEDS WORK`) in `DRF_MIGRATION_URL_MAP.md` and will follow slug-based routing once implemented.