# Objects API endpoints

`ObjectViewSet` exposes `/api/objects/` with pagination plus the shared `count` action. The viewset restricts lists to matched objects (`issues_count > 0`) unless `show-all=yes` is passed.

## List: `GET /api/objects/`
- **Action**: `list`
- **Query params**:
  - `ordering` (`name`,`issues_count`,`volumes_count`); default is `name`.
  - `show-all=yes` disables the default `issues_count > 0` filter.
  - Pagination parameters apply as usual.
- **Response entry**:
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
- **Action**: `retrieve`
- **Response fields** match the list serializer plus any additional detail the serializer exposes (currently same fields).

## `count`: `GET /api/objects/count/`
Returns `{"count": <number>}` applying the same query filters.

## Input payloads
The endpoint is read-only.

## Planned DRF endpoints (status PLAN)
- `GET /api/objects/{slug}/` – replace the Django detail view once slug-based serializers are ready (`NEEDS WORK` in the map).
- `GET /api/objects/{slug}/technical-info/` – expose the object’s comicvine metadata.
- `GET /api/objects/{slug}/start-watch/` – start tracking an object.
- `GET /api/objects/{slug}/stop-watch/` – stop tracking the object.
- `GET /api/objects/{slug}/issues/` – list issues featuring the object.
- `GET /api/objects/{slug}/volumes/` – list volumes containing the object.
- `GET /api/objects/{slug}/issues/{issue_slug}/` – get a specific issue slug for the object.

Each line is currently `PLAN` (with the detail view flagged as `NEEDS WORK`) in `DRF_MIGRATION_URL_MAP.md` and will follow slug-based routing once implemented.
