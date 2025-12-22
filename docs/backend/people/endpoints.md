# People API endpoints

`PeopleViewSet` serves `/api/people/` with the usual count action. Lists are limited to characters with matched issues unless `show-all=yes`.

## List: `GET /api/people/`
- **Action**: `list`
- **Query params**: `ordering` (`name`,`issues_count`,`volumes_count`), `show-all`, pagination.
- **Response example**:
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
- **Action**: `retrieve`
- **Response**: same fields as the list (the serializer does not add extra detail).

## `count`: `GET /api/people/count/`
Returns the matching total.

## Input payloads
Read-only endpoints only.

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
