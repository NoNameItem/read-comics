# Locations API endpoints

All endpoints are powered by [`LocationViewSet`](viewsets.md#locationviewset). The viewset is read-only and exposes standard list/detail operations plus custom `count` and `technical-info` actions.

## List: `GET /api/locations/`

Returns a paginated list of comic book locations with compact metadata. Filters out locations without matched issues by default; use `?show-all=yes` to include all records.

- **ViewSet**: [`LocationViewSet`](viewsets.md#locationviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`LocationsListSerializer`](serializers.md#locationslistserializer)
- **Query params**:
  - `ordering` (`name`, `issues_count`, `volumes_count`). Defaults to `name`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `show-all=yes` returns locations even if no matched issues; default is `no`, which applies `OnlyWithIssuesQuerySetMixin` filter.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "gotham-city",
    "image": "https://.../gotham.jpg",
    "name": "Gotham City",
    "short_description": "Dark, crime-ridden metropolis.",
    "issues_count": 500,
    "volumes_count": 120
  }
  ```

## Detail: `GET /api/locations/{slug}/`

Retrieves comprehensive information about a specific location including aliases, first appearance, and download metadata. Lookup is by URL-safe slug identifier.

- **ViewSet**: [`LocationViewSet`](viewsets.md#locationviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`LocationDetailSerializer`](serializers.md#locationdetailserializer)
- **Path parameter**: `{slug}` (the slug field of the Location model).
- **Response fields** include slug, name, full and square images, list of aliases, start year, first issue name/slug, ComicVine URL, short description, full description, and download links/sizes. Example:
  ```json
  {
    "slug": "gotham-city",
    "name": "Gotham City",
    "image": "https://.../gotham.png",
    "square_image": "https://.../gotham_sq.png",
    "aliases": ["The City"],
    "start_year": 1940,
    "first_issue_name": "Batman #1",
    "first_issue_slug": "batman-1",
    "comicvine_url": "https://comicvine.gamespot.com/gotham-city/4020-41585/",
    "short_description": "Dark, crime-ridden metropolis.",
    "description": "More details...",
    "download_link": "https://example.com/download/gotham.zip",
    "download_size": 1024
  }
  ```

## Count: `GET /api/locations/count/`

Returns the total count of locations after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`LocationViewSet`](viewsets.md#locationviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (applies `OnlyWithIssuesQuerySetMixin` unless `?show-all=yes`).
- **Response**:
  ```json
  {
    "count": 85
  }
  ```

## Technical Info: `GET /api/locations/{slug}/technical-info/`

Exposes administrative metadata about ComicVine synchronization status for the location. Restricted to staff and superuser access only.

- **ViewSet**: [`LocationViewSet`](viewsets.md#locationviewset)
- **Action**: `technical_info` (from `TechnicalInfoActionMixin`)
- **Serializer**: [`ConceptTechnicalInfoSerializer`](serializers.md#concepttechnicalinfoserializer)
- **Path parameter**: `{slug}` (the slug field of the Location model).
- **Permissions**: `IsSuperuserOrStaff` only.
- **Response**:
  ```json
  {
    "id": 1,
    "comicvine_id": 12345,
    "comicvine_status": "Matched",
    "comicvine_last_match": "2025-12-22T12:00:00Z",
    "created_dt": "2020-01-01T00:00:00Z",
    "modified_dt": "2025-12-22T00:00:00Z"
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/locations/{slug}/start-watch/` – track a location in the user's watchlist.
- `GET /api/locations/{slug}/stop-watch/` – remove the location from the watchlist.
- `GET /api/locations/{slug}/issues/` – list issues set in the location.
- `GET /api/locations/{slug}/volumes/` – list volumes tied to the location.
- `GET /api/locations/{slug}/issues/{issue_slug}/` – issue details filtered by location.

Each route has `PLAN` status in `DRF_MIGRATION_URL_MAP.md` and will match the slug-based Django view once serializers are ready.