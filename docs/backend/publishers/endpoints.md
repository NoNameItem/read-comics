# Publishers API endpoints

`PublishersViewSet` handles `/api/publishers/`. It uses `issues_lookup = "volumes__issues"` so counters aggregate all volumes under the publisher. Includes the shared `count` action.

## List: `GET /api/publishers/`
- **Action**: `list`
- **Query params**: `ordering` (`name`,`issues_count`,`volumes_count`), `show-all`, `page`, `page_size`.
- **Response example**:
  ```json
  {
    "slug": "marvel",
    "image": "https://.../marvel.jpg",
    "name": "Marvel",
    "short_description": "Publisher of many IPs.",
    "issues_count": 5000,
    "volumes_count": 300
  }
  ```

## Detail: `GET /api/publishers/{slug}/`
- **Action**: `retrieve`.
- **Response**: same list fields.

## `count`: `GET /api/publishers/count/`
Returns the total after filters.

## Input payloads
No write endpoints are exposed.

## Planned DRF endpoints (status PLAN)
- `GET /api/publishers/{slug}/` – slug detail view expected once serializers map under-the-hood PKs to slugs (`NEEDS WORK` entry).
- `GET /api/publishers/{slug}/technical-info/` – expose ComicVine audit fields for the publisher.
- `GET /api/publishers/{slug}/start-watch/` – add the publisher to the user’s tracked list.
- `GET /api/publishers/{slug}/stop-watch/` – remove the publisher from tracking.
- `GET /api/publishers/{slug}/issues/` – list issues published by the publisher.
- `GET /api/publishers/{slug}/characters/` – list characters tied to the publisher.
- `GET /api/publishers/{slug}/teams/` – list teams under the publisher.
- `GET /api/publishers/{slug}/story-arcs/` – list story arcs belonging to the publisher.
- `GET /api/publishers/{slug}/volumes/` – list volumes published by the publisher.
- `GET /api/publishers/{slug}/issues/{issue_slug}/` – issue-level detail scoped to the publisher.

Each route is `PLAN` in `DRF_MIGRATION_URL_MAP.md` until slug lookups and supporting serializers are in place.
