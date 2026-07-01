# Concepts API endpoints

All endpoints are powered by [`ConceptViewSet`](viewsets.md#conceptviewset). The viewset is read-only and exposes standard list/detail operations plus custom `count` and `technical-info` actions.

## List: `GET /api/concepts/`

Returns a paginated list of comic book concepts with compact metadata. Filters out concepts without matched issues by default; use `?show-all=yes` to include all records.

- **ViewSet**: [`ConceptViewSet`](viewsets.md#conceptviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`ConceptsListSerializer`](serializers.md#conceptslistserializer)
- **Query params**:
  - `ordering` (`name`, `issues_count`, `volumes_count`). Defaults to `name`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `show-all=yes` returns concepts even if no matched issues; default is `no`, which applies `OnlyWithIssuesQuerySetMixin` filter.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "celestial",
    "image": "https://.../celestial.jpg",
    "name": "Celestial",
    "short_description": "Cosmic being.",
    "issues_count": 10,
    "volumes_count": 2
  }
  ```

## Detail: `GET /api/concepts/{slug}/`

Retrieves comprehensive information about a specific concept including aliases, first appearance, and download metadata. Lookup is by URL-safe slug identifier.

- **ViewSet**: [`ConceptViewSet`](viewsets.md#conceptviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`ConceptDetailSerializer`](serializers.md#conceptdetailserializer)
- **Path parameter**: `{slug}` (the slug field of the Concept model).
- **Response fields** include slug, name, full and square images, list of aliases, start year, first issue name/slug, ComicVine URL, short description, full description, and download links/sizes. Example:
  ```json
  {
    "slug": "phoenix-force",
    "name": "Phoenix Force",
    "image": "https://.../phoenix.png",
    "square_image": "https://.../phoenix_sq.png",
    "aliases": ["Of X"],
    "start_year": 1976,
    "first_issue_name": "Uncanny X-Men #101",
    "first_issue_slug": "uncanny-x-men-101",
    "comicvine_url": "https://comicvine.gamespot.com/phoenix-force/4045-287/",
    "short_description": "Near-omnipotent energy.",
    "description": "More details...",
    "download_link": "https://example.com/download/phoenix.zip",
    "download_size": 2048
  }
  ```

## Count: `GET /api/concepts/count/`

Returns the total count of concepts after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`ConceptViewSet`](viewsets.md#conceptviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (applies `OnlyWithIssuesQuerySetMixin` unless `?show-all=yes`).
- **Response**:
  ```json
  {
    "count": 123
  }
  ```

## Technical Info: `GET /api/concepts/{slug}/technical-info/`

Exposes administrative metadata about ComicVine synchronization status for the concept. Restricted to staff and superuser access only.

- **ViewSet**: [`ConceptViewSet`](viewsets.md#conceptviewset)
- **Action**: `technical_info` (from `TechnicalInfoActionMixin`)
- **Serializer**: [`ConceptTechnicalInfoSerializer`](serializers.md#concepttechnicalinfoserializer)
- **Path parameter**: `{slug}` (the slug field of the Concept model).
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

- `GET /api/concepts/{slug}/start-watch/` – add the concept to the active watchlist.
- `GET /api/concepts/{slug}/stop-watch/` – remove the concept from the watchlist.
- `GET /api/concepts/{slug}/issues/` – list issues tied to the concept.
- `GET /api/concepts/{slug}/volumes/` – list volumes tied to the concept.
- `GET /api/concepts/{slug}/issues/{issue_slug}/` – issue details filtered by concept.

Each entry is marked `PLAN` in `DRF_MIGRATION_URL_MAP.md` and will mirror slug-based views after the serializers exist.