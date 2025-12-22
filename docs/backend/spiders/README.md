# Spiders

Handles data import and crawling logic for third-party sources (e.g., ComicVine, other feeds).

## Key modules
- `apps.py` registers the spider service and any related signals.
- `tasks.py` defines background jobs that run crawler workflows.
- `templates/` and `views.py` (if present) expose progress dashboards or manual triggers.
- `management/` commands wrap crawler runs and data refresh jobs.
