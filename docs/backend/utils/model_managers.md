# Managers defined in `utils/model_managers.py`

## Summary
- [`ComicvineSyncQuerySet`](#comicvinesyncqueryset) — custom queryset that orchestrates Comicvine syncing, matches, and queue helpers. See the [Reference](#reference) entries for field/method details.
- [`ComicvineSyncManager`](#comicvinesyncmanager) — manager based on the above queryset via `BaseManager.from_queryset`; see the [Reference](#reference) entry for details.

## Reference

### `ComicvineSyncQuerySet`
- Extends `models.QuerySet` with helpers that drive the shared Comicvine sync flow used by all derived models.

#### Methods
- `get_or_create_from_comicvine(self, comicvine_id, defaults=None, force_refresh=False, follow_m2m=True, delay=False)`
  - `comicvine_id`: Required Comicvine identifier.
  - `defaults`: Dict of fallback field values passed to Django's `get_or_create`.
  - `force_refresh`: When `True`, the method triggers `fill_from_comicvine` even for existing records (as long as they are not queued).
  - `follow_m2m`: Passed to `fill_from_comicvine` to control whether ManyToMany relations should be populated.
  - `delay`: If `True`, the configured Celery task is used instead of running sync synchronously.
  - Returns a tuple `(instance, created, matched_flag)` mirroring Django's `get_or_create` plus a flag that indicates whether Comicvine data was matched.
- `matched(self)`: Filters the queryset to objects whose `comicvine_status` is `MATCHED`.
- `not_matched(self)`: Filters for the `NOT_MATCHED` status.
- `queued(self)`: Filters for the `QUEUED` status.
- `was_matched(self)`: Filters records that have a non-null `comicvine_last_match` timestamp.

### `ComicvineSyncManager`
- Subclasses Django's manager via `BaseManager.from_queryset(ComicvineSyncQuerySet)` so every model inheriting it gets the helper methods defined above.
- No additional methods are defined; `pass` is present to keep the manager declaration explicit.
