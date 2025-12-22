# Volumes

Manages series and volumes, linking issue numbers with external metadata.

## Key modules
- `models.py` and `view_mixins.py` describe volume data and reusable view logic.
- `search_adapters.py` and `api/` provide search and REST endpoints for volumes.
- `tasks.py` automates importing and refreshing series data.
- `templates/`, `views.py`, and `static/` render volume cards, lists, and styles.
