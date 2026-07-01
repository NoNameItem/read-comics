# Search API endpoints

Currently, there is no DRF-powered search endpoint implemented. Search functionality is still handled by Django views.

## Planned DRF endpoints (status PLAN)

The following endpoints are planned to replace the existing Django search views:

### Search: `GET /api/search/`

Will provide full-text search across multiple content types (issues, volumes, characters, teams, etc.).

- **ViewSet**: To be implemented
- **Action**: To be defined (likely custom search action)
- **Serializer**: To be defined
- **Query params**:
  - `q` (search query string)
  - Additional filtering and pagination parameters
- **Response structure**: Will return search results grouped by content type with pagination support.

### AJAX Search: `GET /api/search/ajax/`

Will provide autocomplete/suggestions for search queries, typically used for dropdown search boxes.

- **ViewSet**: To be implemented
- **Action**: To be defined (likely custom suggestions action)
- **Serializer**: To be defined
- **Query params**:
  - `q` (partial search query string)
  - `limit` (maximum number of suggestions to return)
- **Response structure**: Will return quick suggestion results for autocomplete functionality.

## Current implementation

Search is currently handled by Django views at:
- `/search/` - Full search results page
- `/search/ajax/` - AJAX autocomplete endpoint

These endpoints are marked as `PLAN` in `DRF_MIGRATION_URL_MAP.md` and will be migrated to DRF once the search infrastructure is redesigned. The new endpoints will mirror the current Django search behaviors (HTML results and AJAX suggestions) while providing a proper REST API interface with consistent query params and pagination logic.