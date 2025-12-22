# Volumes API endpoints

`VolumesViewSet` serves `/api/volumes/` with finished/started annotations plus the shared `count` and `started` endpoints.

## List: `GET /api/volumes/`
- **Action**: `list`
- **Query params**:
  - `ordering` (`start_year`,`name`,`issues_count`). Defaults to `start_year`.
  - `hide-finished=yes` filters out volumes where the user read every issue.
  - `show-all=yes` removes the implicit `issues_count > 0` filter.
  - Pagination parameters are supported.
- **Response sample**:
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
- **Action**: `retrieve`
- **Response**: same fields as list.

## `count`: `GET /api/volumes/count/`
Returns the total number of volumes matching the filters.

## `started`: `GET /api/volumes/started/`
- **Action**: `started`
- **Permissions**: authenticated users only.
- **Description**: returns volumes with `is_started=True` and `is_finished=False`, sorted by `-max_finished_date`.
- **Response example**:
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
Volume endpoints are read-only.

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
