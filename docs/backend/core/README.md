# Core

Delivers the main site pages, templates, and shared data collectors.

## Key modules
- `views.py`, `urls.py`, and `templates/` house the homepage, sitemap, status pages (404/500), and general layouts.
- `api/` exposes REST endpoints that aggregate data from several apps.
- `collectors/` contains logic for statistics gathering and syncing external sources with internal models.
