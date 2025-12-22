# Story Arcs

Manages story arcs, including chronology and key events.

## Key modules
- `models.py` defines a story arc model with links to issues and characters.
- `search_adapters.py` and `api/` cover indexing and REST access for arcs.
- `sublist_querysets.py` and `tasks.py` provide helper querysets and background updates.
- `templates/`, `views.py`, and `static/` deliver arc detail pages and supporting styles.
