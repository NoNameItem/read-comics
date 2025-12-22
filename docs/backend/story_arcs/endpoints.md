# Story arcs API endpoints

`StoryArcsViewSet` exposes `/api/story-arcs/` with filters for started/finished state plus `count` and `started` actions.

## List: `GET /api/story-arcs/`
- **Action**: `list`
- **Query params**:
  - `ordering` (`name`,`issues_count`,`volumes_count`). Defaults to `name`.
  - `show-all=yes` bypasses the default `issues_count > 0` policy.
  - `hide-finished=yes` (default) filters out arcs where the current user finished every issue; set `hide-finished=no` to include completed arcs.
  - Pagination params apply as usual.
- **Response example**:
  ```json
  {
    "slug": "infinity-gauntlet",
    "image": "https://.../gauntlet.jpg",
    "publisher": {"name": "Marvel", "image": "https://...", "slug": "marvel"},
    "name": "Infinity Gauntlet",
    "short_description": "The cosmic gauntlet event.",
    "issues_count": 6,
    "finished_count": 1,
    "volumes_count": 2,
    "is_finished": false
  }
  ```

## Detail: `GET /api/story-arcs/{slug}/`
- **Action**: `retrieve`
- **Response**: same serializer fields as list (no separate detail serializer currently).

## `count`: `GET /api/story-arcs/count/`
Returns the total matching arcs after applying `hide-finished` and other query params.

## `started`: `GET /api/story-arcs/started/`
- **Action**: `started`
- **Permissions**: authenticated only.
- **Description**: returns arcs the user has begun but not finished, ordered by `-max_finished_date`.
- **Response example**:
  ```json
  {
    "slug": "dark-knight-returns",
    "display_name": "The Dark Knight Returns",
    "image": "https://.../dkr.jpg",
    "max_finished_date": "2024-06-01T12:00:00Z",
    "finished_count": 2,
    "issues_count": 4
  }
  ```

## Input payloads
No write actions exposed.

## Planned DRF endpoints (status PLAN)
- `GET /api/story-arcs/{slug}/` (detail serializer/detail slug lookup needs work; map lists as `NEEDS WORK`).
- `GET /api/story-arcs/{slug}/technical-info/`
- `GET /api/story-arcs/{slug}/start-watch/`
- `GET /api/story-arcs/{slug}/stop-watch/`
- `GET /api/story-arcs/{slug}/mark-finished/`
- `GET /api/story-arcs/{slug}/died/`
- `GET /api/story-arcs/{slug}/authors/`
- `GET /api/story-arcs/{slug}/characters/`
- `GET /api/story-arcs/{slug}/concepts/`
- `GET /api/story-arcs/{slug}/disbanded/`
- `GET /api/story-arcs/{slug}/first-appearances/`
- `GET /api/story-arcs/{slug}/issues/{issue_slug}/`
- `GET /api/story-arcs/{slug}/locations/`
- `GET /api/story-arcs/{slug}/issues/`
- `GET /api/story-arcs/{slug}/objects/`
- `GET /api/story-arcs/{slug}/teams/`
- `GET /api/story-arcs/{slug}/volumes/`

All these paths are marked `PLAN` (and the detail endpoint as `NEEDS WORK`) in `DRF_MIGRATION_URL_MAP.md`, pending slug-based detail+serializers.
