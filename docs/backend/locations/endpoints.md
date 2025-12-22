# Locations API endpoints

`LocationViewSet` powers `/api/locations/` and includes the shared `count`/`technical-info` actions.

## List: `GET /api/locations/`
- **Action**: `list`
- **Query params**: `ordering` (`name`,`issues_count`,`volumes_count`), `show-all=yes`, plus DRF pagination.
- **Response** entry example:
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
- **Action**: `retrieve`
- **Payload**: slug path parameter.
- **Fields** include slug, name, full/square images, aliases, start year, first issue metadata, ComicVine URL, descriptions, download link/size.

## `count`: `GET /api/locations/count/`
Returns the same filtered total as the list view.

## `technical-info`: `GET /api/locations/{slug}/technical-info/`
- Staff-only.
- Returns `id`, `comicvine_id`, status, last match, and audit timestamps.

## Input payloads
Read-only endpoints only.

## Planned DRF endpoints (status PLAN)
- `GET /api/locations/{slug}/start-watch/` – track a location in the user’s watchlist.
- `GET /api/locations/{slug}/stop-watch/` – remove the location from the watchlist.
- `GET /api/locations/{slug}/issues/` – list issues set in the location.
- `GET /api/locations/{slug}/volumes/` – list volumes tied to the location.
- `GET /api/locations/{slug}/issues/{issue_slug}/` – issue details filtered by location.

Each route has `PLAN` status in `DRF_MIGRATION_URL_MAP.md` and will match the slug-based Django view once serializers are ready.
