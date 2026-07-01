# Base models in `utils/models.py`

## Summary
- [`ComicvineSyncModel`](#comicvinesyncmodel) — high-level abstract model for syncing domain data with Comicvine that tracks status, timestamps, and exposes helpers like `fill_from_comicvine`. See the [Reference](#reference) entries for all fields and methods.
- [`ComicvineSyncModelConfigurationError`](#comicvinesyncmodelconfigurationerror) — raised when field mappings or helper hooks are misconfigured. See the [Reference](#reference) entries for details.

## `ComicvineSyncModel`
- Abstract Django model that stores Comicvine integration metadata (IDs, URLs, status, timestamps) and exposes `logger`/`manager` support.
- Tracks `comicvine_status` (Not matched, Queued, Matched) plus the last match timestamp and automatic `modified_dt` updates.
- Uses [ComicvineSyncManager](model_managers.md#comicvinesyncmanager) to provide helpers for syncing and queueing API work.
- Implements `fill_from_comicvine`, `get_document_from_api`, and `process_document` utilities to fetch data from Mongo/Comicvine, handle rate limits, and queue background jobs.
- Field mapping is customizable via `FIELD_MAPPING` and `_DEFAULT_FIELDS_MAPPING`, enabling derived models to map Comicvine JSON keys to model fields with optional helper methods (`strip_links`, `get_issue`, `get_character`, etc.).

## Document helpers
- `_fill_field_from_document` inspects Django field types and delegates to `_set_non_m2m_from_document` or `_set_m2m_from_document` depending on ManyToMany relationships.
- `_get_value_by_path` traverses nested JSON paths, logging when keys or indexes cannot be found.
- `pre_save`/`post_save` hook points allow subclasses to plug into the save lifecycle.

## Integration helpers
- Static helpers like `get_issue`, `get_character`, `get_concept`, etc., lazily import the corresponding app models and create placeholder records via `get_or_create_from_comicvine`.
- `description` property sanitizes HTML descriptions and reflows lazy-loaded images for display.

## Reference

### `ComicvineSyncModelConfigurationError`
- A custom exception that signals a misconfiguration of field mappings or helper methods when processing Comicvine payloads.

### `ComicvineSyncModel`
- Abstract Django model that standardizes how domain models synchronize with Comicvine data, storing identifiers, status, and timestamps while providing shared helper methods for fetching, queuing, and persisting external documents.

#### Class attributes
- `MONGO_COLLECTION`: MongoDB collection name that child models must set.
- `MONGO_PROJECTION`: Optional projection dict to limit fields from Mongo.
- `_DEFAULT_FIELDS_MAPPING`: Base mapping for converting Comicvine JSON keys to Django fields (name, aliases, descriptions, images, first issue data).
- `COMICVINE_INFO_TASK`: Optional Celery task used for deferred syncing.
- `COMICVINE_API_URL`: API URL template for fetching Comicvine detail payloads.
- `COMICVINE_FORCE_DETAIL_INFO`: Flag to control when detail data is forced.
- `logger`: Instance of `Logger` (default `comicvine-sync` logger) used for structured messages.
- `objects`: `ComicvineSyncManager` that encapsulates helper querysets and queue operations.

#### Model fields
- `comicvine_id` (`IntegerField`, unique): Comicvine identifier for the record.
- `comicvine_url` (`URLField`, nullable): Public Comicvine URL for reference.
- `comicvine_status` (`CharField` with `ComicvineStatus` choices): Tracks whether the record is matched, queued, or unmatched.
- `comicvine_last_match` (`DateTimeField`, nullable): Timestamp of the last successful match.
- `created_dt`/`modified_dt` (`DateTimeField`): Automatic creation/modification timestamps; `modified_dt` is refreshed whenever tracker detects changes.

#### Inner helpers
- `ComicvineStatus` (`TextChoices`): Defines `NOT_MATCHED`, `QUEUED`, and `MATCHED` states.

#### Lifecycle methods
- `__init__`: Ensures the logger exists on instantiation.
- `save(self, force_insert=False, force_update=False, using=None, update_fields=None)`: Wraps Django’s `save`, calling `pre_save`, updating `modified_dt` when tracker detects changes, and invoking `post_save`. Parameters mirror Django’s API to preserve compatibility with transactions and update optimization.
- `pre_save(self, force_insert=False, force_update=False, using=None, update_fields=None)`: Hook invoked before saving; override to customize behavior without altering the default workflow. Parameters match Django’s `Model.save`.
- `post_save(self)`: Hook invoked after the base `save`; override to run side effects once the model has been persisted.

#### Sync helpers
- `get_document_from_api`: Requests the Comicvine API (with retry/backoff), stores the response in Mongo, and returns the document; no parameters.
- `fill_from_comicvine(self, follow_m2m=True, delay=False, force_api_refresh=False)`: Coordination method that reads from Mongo or queues a background job to fetch from the API, including waiting on `APIQueue` and `Locks` models.
  - `follow_m2m`: When `True`, ManyToMany relations are populated; `False` keeps them untouched.
  - `delay`: When `True`, the configured Celery task (`COMICVINE_INFO_TASK`) is used to defer syncing.
  - `force_api_refresh`: Bypasses the Mongo cache and forces a fresh API call.
- `process_document(self, document, follow_m2m)`: Applies the field mapping to a fetched document, optionally following M2M relations; `document` is the Comicvine payload and `follow_m2m` controls whether relations are resolved.
- `get_field_mapping(self)`: Merges `_DEFAULT_FIELDS_MAPPING` with `FIELD_MAPPING` declared on child models, returning the effective mapping dictionary.

#### Field/document helpers
- `_fill_field_from_document(self, document, field, source, follow_m2m)`: Routes a mapped field to the correct setter depending on whether it is an `ManyToManyField`.
  - `document`: Comicvine payload dict.
  - `field`: Name of the Django field being populated.
  - `source`: Mapping entry (string path or dict with method/path overrides).
  - `follow_m2m`: Whether ManyToMany relationships should be applied.
- `_set_non_m2m_from_document(self, document, field, method, path)`: Extracts a value (and optional converter) from the document path and assigns it to the model field.
  - `method`: Optional callable that post-processes the extracted value.
  - `path`: Dot-notation path into the Comicvine payload.
- `_set_m2m_from_document(self, document, field, path, inner_path, method, override)`: Adds related objects to an M2M field, optionally overriding the existing set, and supports custom converter methods that return `(value, defaults)`.
  - `inner_path`: Dot-notation path inside each list item if only a nested field is required.
  - `override`: When `True`, the existing relation set is cleared before adding new entries.
- `_get_value_by_path(self, document, path)`: Traverses nested JSON paths (dot notation) with logging for missing keys or indexes.
  - `path`: Dot-separated path (e.g., `image.small_url`).

#### Utility helpers
- `strip_links`: Removes `<a>` tags from rich HTML descriptions.
- `get_issue_name(self, comicvine_id)`: Builds a human-readable issue name by consulting cached Mongo records; `comicvine_id` is required.
- `get_issue(comicvine_id)`: Looks up a local `Issue` by Comicvine ID; raises `Issue.DoesNotExist` if missing.
- `get_character(d)`: Resolves a character dictionary (`d`) into a `Character` instance, queuing creation if needed; expects `d["id"]`.
- `get_concept(d)`: Resolves a concept dictionary into a `Concept`.
- `get_location(d)`: Resolves a location dict into a `Location`.
- `get_object(d)`: Resolves an object dict into an `Object`.
- `get_power(d)`: Resolves a power dict into a `Power`.
- `get_story_arc(d)`: Resolves a story arc dict into a `StoryArc`.
- `get_team(d)`: Resolves a team dict into a `Team`.
- `get_volume(d)`: Resolves a volume dict into a `Volume`.
- `get_publisher(d)`: Resolves a publisher dict into a `Publisher`.
- `get_person(d)`: Resolves a person dict into a `Person`.

#### Convenience properties
- `comicvine_actual`: Indicates whether the stored document is still current compared to Mongo’s crawl timestamp.
- `comicvine_document`: Loads the cached Mongo document for the record.
- `description`: Sanitizes HTML descriptions (fixing lazy-loaded images) for display.
- `meta`: Shortcut to `_meta`.
- `display_name`: String representation intended for UI use (calls `__str__`).
