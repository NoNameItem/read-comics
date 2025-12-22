# Issues API endpoints

`IssueViewSet` exposes `/api/issues/` and supports `count`/`technical-info` actions for staff.

## List: `GET /api/issues/`
- **Action**: `list`
- **Default behavior** hides issues already finished by the current user (`?hide-finished=yes`). Pass `?hide-finished=no` to include completed issues.
- **Ordering** supports `cover_date`, `volume__name`, `volume__start_year`, `numerical_number`, and `number`. Defaults to `cover_date` then volume metadata.
- **Response** (paginated) example entry:
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
- **Authentication note**: when logged in, the list adds `finished_flg` and filters accordingly; unauthenticated users receive `null`.

## Detail: `GET /api/issues/{slug}/`
- **Action**: `retrieve`, lookup by slug.
- **Additional context**: detail serializer returns the same nested volume/publisher data plus `number`, `volume_last_number`, `name`, `cover_date`, `store_date`, `description`, `download_link`, `download_size`, `is_finished`, `prev_issue_slug`, `next_issue_slug`, `number_in_sublist`, and `total_in_sublist`.
- **Example**:
  ```json
  {
    "slug": "detective-comics-27",
    "image": "https://.../dc27.jpg",
    "square_image": "https://.../dc27_square.jpg",
    "publisher": {...},
    "volume": {...},
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

## `count`: `GET /api/issues/count/`
Applies the same `hide-finished` and ordering filters before returning `{"count": 870}`.

## `technical-info`: `GET /api/issues/{slug}/technical-info/`
- Requires staff/superuser.
- Response mirrors the serializer described in `docs/backend/api-endpoints.md` (ID, ComicVine metadata, timestamps).

## Input payloads
All endpoints are read-only (no POST/PATCH/DELETE).

## Planned DRF endpoints (status PLAN)
- `POST /api/issues/{slug}/mark-read/` – toggle the user’s “read” status for the issue.
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
