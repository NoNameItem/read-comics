# Utils

Common utilities shared across other Django apps.

- [Base models](models.md) (see `ComicvineSyncModel`, field helpers, and queue logic).
- [Model managers](model_managers.md) (details on `ComicvineSyncQuerySet` and `ComicvineSyncManager`).
- [Model mixins](model_mixins.md) (image helpers, alias utilities, download-size helpers).
- [Tasks](tasks.md) and [Comicvine stats](comicvine_stats.md) — background jobs and ComicVine helpers.
- `api/`, `views.py`, and `view_mixins.py` — REST helpers, reusable views, and serializer mixins.
- `templatetags/`, `form_helpers.py`, `context_processors.py` — template tags, form helpers, and context data for the UI.
