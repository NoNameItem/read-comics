# Issues API endpoints

All endpoints are powered by [`IssueViewSet`](viewsets.md#issueviewset). The viewset is read-only and exposes standard list/detail operations plus custom `count` and `technical-info` actions.

## List: `GET /api/issues/`

Returns a paginated list of comic book issues with publisher and volume metadata. By default, hides issues already finished by the current user; use `?hide-finished=no` to include completed issues.

- **ViewSet**: [`IssueViewSet`](viewsets.md#issueviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`IssuesListSerializer`](serializers.md#issueslistserializer)
- **Query params**:
  - `ordering` (`cover_date`, `volume__name`, `volume__start_year`, `numerical_number`, `number`). Defaults to `cover_date`, then volume metadata. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `hide-finished=yes` (default) filters out issues completed by the authenticated user; use `hide-finished=no` to include all issues.
  - DRF pagination params (`page`, `page_size`).
- **Authentication note**: When logged in, the list adds `finished_flg` and filters accordingly; unauthenticated users receive `null`.
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "batman-1",
    "image": "https://.../batman1.jpg",
    "publisher": {"name": "DC", "image": "https://...", "slug": "dc"},
    "name": "Batman #1",
    "short_description": "Bruce Wayne returns.",
    "cover_date": "1950-05-01",
    "volume": {"slug": "detective-comics", "display_name": "Detective Comics", "start_year": 1937, "name": "Detective Comics"},
    "is_finished": false
  }
  ```

## Detail: `GET /api/issues/{slug}/`

Retrieves comprehensive information about a specific issue including cover/store dates, description, download metadata, and navigation links to previous/next issues. Lookup is by URL-safe slug identifier.

- **ViewSet**: [`IssueViewSet`](viewsets.md#issueviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`IssueDetailSerializer`](serializers.md#issuedetailserializer)
- **Path parameter**: `{slug}` (the slug field of the Issue model).
- **Response fields** include slug, full/square images, publisher, volume, issue number, volume last number, name, cover date, store date, descriptions, ComicVine URL, download link/size, finished status, previous/next issue slugs, and position within filtered list. Example:
  ```json
  {
    "slug": "detective-comics-27",
    "image": "https://.../dc27.jpg",
    "square_image": "https://.../dc27_square.jpg",
    "publisher": {"name": "DC", "image": "https://...", "slug": "dc"},
    "volume": {"slug": "detective-comics", "display_name": "Detective Comics", "start_year": 1937, "name": "Detective Comics"},
    "number": "27",
    "volume_last_number": "870",
    "name": "Detective Comics #27",
    "cover_date": "1939-05-01",
    "store_date": "1939-05-01",
    "short_description": "First appearance of Batman.",
    "description": "Detailed issue notes...",
    "comicvine_url": "https://...",
    "download_link": "https://...",
    "download_size": 512,
    "is_finished": false,
    "prev_issue_slug": null,
    "next_issue_slug": "detective-comics-28",
    "number_in_sublist": 1,
    "total_in_sublist": 870
  }
  ```

## Count: `GET /api/issues/count/`

Returns the total count of issues after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`IssueViewSet`](viewsets.md#issueviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (applies `hide-finished` filter by default).
- **Response**:
  ```json
  {
    "count": 870
  }
  ```

## Technical Info: `GET /api/issues/{slug}/technical-info/`

Exposes administrative metadata about ComicVine synchronization status for the issue. Restricted to staff and superuser access only.

- **ViewSet**: [`IssueViewSet`](viewsets.md#issueviewset)
- **Action**: `technical_info` (from `TechnicalInfoActionMixin`)
- **Serializer**: [`IssueTechnicalInfoSerializer`](serializers.md#issuetechnicalinfoserializer)
- **Path parameter**: `{slug}` (the slug field of the Issue model).
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

- `POST /api/issues/{slug}/mark-read/` – toggle the user's "read" status for the issue.
- `GET /api/issues/{slug}/characters/` – list characters appearing in the issue.
- `GET /api/issues/{slug}/characters-died/` – list characters who died in the issue.
- `GET /api/issues/{slug}/concepts/` – list concepts featured in the issue.
- `GET /api/issues/{slug}/locations/` – list locations appearing in the issue.
- `GET /api/issues/{slug}/objects/` – list objects appearing in the issue.
- `GET /api/issues/{slug}/authors/` – list creators for the issue.
- `GET /api/issues/{slug}/story-arcs/` – list story arcs that include the issue.
- `GET /api/issues/{slug}/teams/` – list teams appearing in the issue.
- `GET /api/issues/{slug}/disbanded-teams/` – list teams introduced but later disbanded.
- `GET /api/issues/{slug}/first-appearances/` – list characters making their first appearance in the issue.

All entries match `PLAN` in `DRF_MIGRATION_URL_MAP.md` and will switch to slug-aware serializers once the related serializers/detail behavior is stable.