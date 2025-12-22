# Teams

Tracks groups of characters and provides search-friendly listings.

## Key modules
- `models.py` and `sublist_querysets.py` define team models and helper selection logic for lists.
- `search_adapters.py`, `api/`, and `views.py` expose search indexes, REST endpoints, and front-end views.
- `tasks.py` handles background updates and relationship syncs with other entities.
- `templates/` render team rosters and detail screens.
