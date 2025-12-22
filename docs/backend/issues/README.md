# Issues

Handles comic issues, their numbering, release dates, and related metadata.

## Key modules
- `models.py` stores issue numbers, dates, and volume context.
- `search_adapters.py`, `api/`, and `view_mixins.py` provide search, REST, and flexible display logic.
- `tasks.py` takes care of import jobs, synchronization, and data aggregation.
- `templates/` and `views.py` render issue lists, detail pages, and filters.
