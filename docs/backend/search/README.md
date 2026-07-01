# Search

Centralizes global search logic and interfaces for quick access to project data.

## Key modules
- [`search_adapters.py`](search_adapters.md) provides [`BaseSearchAdapter`](search_adapters.md#basesearchadapter) for consistent django-watson integration across all searchable models.
- `views.py`, `templates/`, and `urls.py` provide public search interactions.
- `api/` and `migrations/` include REST helpers and index persistence.
