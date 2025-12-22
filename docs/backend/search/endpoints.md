# Search API plans

There is no DRF-powered search endpoint yet, but `DRF_MIGRATION_URL_MAP.md` lists the `/search/` and `/search/ajax/` Django views as `PLAN`. When these are migrated, they will likely live under:

- `GET /api/search/`
- `GET /api/search/ajax/`

The endpoints should mirror the current Django search behaviors (HTML results and the AJAX suggestions screen) while reusing the same query params and pagination logic once implemented.
