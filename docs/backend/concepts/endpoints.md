# Concepts API endpoints

`ConceptViewSet` provides `/api/concepts/` with read-only access and the shared `count`/`technical-info` actions.

## List: `GET /api/concepts/`
- **Action**: `list`
- **Query params**:
  - `ordering` (`name`,`issues_count`,`volumes_count`). Defaults to `name`.
  - `show-all=yes` lifts the implicit `issues_count > 0` filter.
  - DRF pagination parameters are supported (`page`, `page_size`).
- **Response** (paginated):
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
- **Action**: `retrieve`, lookup by slug.
- **Fields** include slug, name, full/square images, aliases, start year, first issue metadata, ComicVine link, short and full descriptions, download link/size.
- **Example**:
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

## `count` action: `GET /api/concepts/count/`
Returns the filtered count, same behavior as the list endpoint.

## `technical-info` action: `GET /api/concepts/{slug}/technical-info/`
- Requires staff/superuser.
- Returns `id`, `comicvine_id`, display status, last match timestamp, and audit timestamps.

## Input payloads
The viewset is read-only (no POST, PATCH, DELETE).

## Planned DRF endpoints (status PLAN)
- `GET /api/concepts/{slug}/start-watch/` – add the concept to the active watchlist.
- `GET /api/concepts/{slug}/stop-watch/` – remove the concept from the watchlist.
- `GET /api/concepts/{slug}/issues/` – list issues tied to the concept.
- `GET /api/concepts/{slug}/volumes/` – list volumes tied to the concept.
- `GET /api/concepts/{slug}/issues/{issue_slug}/` – issue details filtered by concept.

Each entry is marked `PLAN` in `DRF_MIGRATION_URL_MAP.md` and will mirror slug-based views after the serializers exist.
