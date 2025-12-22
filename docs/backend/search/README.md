# Search

Centralizes global search logic and interfaces for quick access to project data.

## Key modules
- `search_adapters.py` connects to Watson and other indexes.
- `views.py`, `templates/`, and `urls.py` provide public search interactions.
- `api/` and `migrations/` include REST helpers and index persistence.
