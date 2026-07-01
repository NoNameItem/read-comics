# People API endpoints

All endpoints are powered by [`PeopleViewSet`](viewsets.md#peopleviewset). The viewset is read-only and exposes standard list/detail operations plus a custom `count` action.

## List: `GET /api/people/`

Returns a paginated list of comic book people/creators with compact metadata. Filters out people without matched issues by default; use `?show-all=yes` to include all records.

- **ViewSet**: [`PeopleViewSet`](viewsets.md#peopleviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`PeopleListSerializer`](serializers.md#peoplelistserializer)
- **Query params**:
  - `ordering` (`name`, `issues_count`, `volumes_count`). Defaults to `name`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `show-all=yes` returns people even if no matched issues; default is `no`, which applies `OnlyWithIssuesQuerySetMixin` filter.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "tony-stark",
    "image": "https://.../tony.jpg",
    "name": "Tony Stark",
    "short_description": "Iron Man persona.",
    "issues_count": 80,
    "volumes_count": 20
  }
  ```

## Detail: `GET /api/people/{slug}/`

Retrieves information about a specific person/creator. Currently returns the same fields as the list endpoint.

- **ViewSet**: [`PeopleViewSet`](viewsets.md#peopleviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`PeopleListSerializer`](serializers.md#peoplelistserializer)
- **Path parameter**: `{slug}` (the slug field of the Person model).
- **Response fields**: Same as list endpoint above.

## Count: `GET /api/people/count/`

Returns the total count of people after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`PeopleViewSet`](viewsets.md#peopleviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (applies `OnlyWithIssuesQuerySetMixin` unless `?show-all=yes`).
- **Response**:
  ```json
  {
    "count": 150
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/people/{slug}/` – slug-based detail endpoint pending slug lookup (map marks as `NEEDS WORK`).
- `GET /api/people/{slug}/technical-info/` – return ComicVine metadata.
- `GET /api/people/{slug}/start-watch/` – add the person to the watchlist.
- `GET /api/people/{slug}/stop-watch/` – remove the person from the watchlist.
- `GET /api/people/{slug}/issues/` – list issues featuring the person.
- `GET /api/people/{slug}/volumes/` – list volumes that include the person.
- `GET /api/people/{slug}/characters/` – list related characters.
- `GET /api/people/{slug}/issues/{issue_slug}/` – issue detail scoped to the person.

Each entry is marked `PLAN` in `DRF_MIGRATION_URL_MAP.md` until slug lookups/serializers are ready.