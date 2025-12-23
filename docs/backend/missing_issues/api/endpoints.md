# Missing issues API endpoints

All endpoints are powered by [`MissingIssueViewSet`](viewsets.md#missingissueviewset). The viewset is read-only and exposes standard list/detail operations plus a custom `count` action. Only issues with `skip=False` are shown.

## List: `GET /api/missing-issues/`

Returns a paginated list of missing comic book issues that need tracking. Automatically filters to show only issues where `skip=False`.

- **ViewSet**: [`MissingIssueViewSet`](viewsets.md#missingissueviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: Uses default `ModelSerializer` (no custom serializer defined)
- **Query params**: Standard DRF pagination params (`page`, `page_size`). No custom ordering or filtering.
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": null,
    "id": 123,
    "comicvine_id": 456789,
    "name": "Amazing Issue",
    "number": "1",
    "numerical_number": 1.0,
    "cover_date": "1970-01-01",
    "volume_name": "Amazing Comics",
    "volume_start_year": "1970",
    "publisher_name": "Marvel",
    "characters": [1, 2],
    "concepts": [3],
    "locations": [4],
    "objects_in": [5],
    "people": [6],
    "story_arcs": [7],
    "teams": [8],
    "volume": 9,
    "publisher": 10,
    "skip": false,
    "skip_date": null
  }
  ```

Note: Related fields (`characters`, `concepts`, etc.) return lists of related primary keys because there is no custom serializer.

## Detail: `GET /api/missing-issues/{pk}/`

Retrieves comprehensive information about a specific missing issue. Lookup is by database primary key (not slug).

- **ViewSet**: [`MissingIssueViewSet`](viewsets.md#missingissueviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: Uses default `ModelSerializer` (no custom serializer defined)
- **Path parameter**: `{pk}` (the primary key/ID of the MissingIssue model).
- **Response fields**: Returns all `MissingIssue` model fields, including `comicvine_url`, `volume_comicvine_id`, and `publisher_comicvine_id`.

## Count: `GET /api/missing-issues/count/`

Returns the total count of missing issues after applying filters. Respects the `skip=False` filter.

- **ViewSet**: [`MissingIssueViewSet`](viewsets.md#missingissueviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: No additional filtering available.
- **Response**:
  ```json
  {
    "count": 342
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/missing-issues/do-space/` – sync missing issues from DigitalOcean Spaces.
- `POST /api/missing-issues/purge-deleted/` – remove stale deleted records from the queue.
- `GET /api/missing-issues/ignored-issues/` – list user-ignored issues.
- `GET /api/missing-issues/ignored-volumes/` – list ignored volumes.
- `GET /api/missing-issues/ignored-publishers/` – list ignored publishers.
- `POST /api/missing-issues/ignored-issues/{pk}/delete/` – delete a specific ignored issue record after review.
- `POST /api/missing-issues/ignored-volumes/{pk}/delete/` – delete an ignored volume entry.
- `POST /api/missing-issues/ignored-publishers/{pk}/delete/` – delete an ignored publisher entry.
- `POST /api/missing-issues/skip-issue/{comicvine_id}/` – mark a ComicVine issue as intentionally skipped.
- `POST /api/missing-issues/skip-volume/{comicvine_id}/` – skip the entire volume.
- `POST /api/missing-issues/skip-publisher/{comicvine_id}/` – skip all issues from a publisher.
- `POST /api/missing-issues/ignore-issue/{comicvine_id}/` – move an issue to the ignored list.
- `POST /api/missing-issues/ignore-volume/{comicvine_id}/` – ignore a full volume.
- `POST /api/missing-issues/ignore-publisher/{comicvine_id}/` – ignore a publisher.
- `POST /api/missing-issues/reload-from-do/` – reload missing issue data from DO Spaces.
- `GET /api/missing-issues/watched/` – list watched missing issues.
- `POST /api/missing-issues/watched/skip-issue/{comicvine_id}/` – skip an issue on the watched list.
- `POST /api/missing-issues/watched/skip-volume/{comicvine_id}/` – skip a watched volume.
- `POST /api/missing-issues/watched/skip-publisher/{comicvine_id}/` – skip watched publisher issues.
- `POST /api/missing-issues/watched/ignore-issue/{comicvine_id}/` – ignore a watched issue.
- `POST /api/missing-issues/watched/ignore-volume/{comicvine_id}/` – ignore a watched volume.
- `POST /api/missing-issues/watched/ignore-publisher/{comicvine_id}/` – ignore a watched publisher.
- `GET /api/<category_plural>/<slug>/missing-issues/` – list missing issues for the given category (characters, volumes, etc.).
- `POST /api/<category_plural>/<slug>/missing-issues/skip-issue/{comicvine_id}/` – skip an issue within the contextual category.
- `POST /api/<category_plural>/<slug>/missing-issues/skip-volume/{comicvine_id}/` – skip a volume associated with the category slug.
- `POST /api/<category_plural>/<slug>/missing-issues/skip-publisher/{comicvine_id}/` – skip the publisher in context.
- `POST /api/<category_plural>/<slug>/missing-issues/ignore-issue/{comicvine_id}/` – ignore an issue while viewing the category.
- `POST /api/<category_plural>/<slug>/missing-issues/ignore-volume/{comicvine_id}/` – ignore a contextual volume.
- `POST /api/<category_plural>/<slug>/missing-issues/ignore-publisher/{comicvine_id}/` – ignore a contextual publisher.

These `PLAN` entries mirror the specialized missing-issues flows listed in `DRF_MIGRATION_URL_MAP.md` and await serializer/view implementations.