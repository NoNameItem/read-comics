# Tasks defined in `utils/tasks.py`

## Summary
- [`WrongKeyFormatError`](#wrongkeyformaterror) — exception raised when an S3 key doesn’t match the expected pattern; see the [Reference](#reference) entry for where it is used.
- [`BaseSpaceTask`](#basespacetask) — scans DigitalOcean Space prefixes and queues entry-level tasks; details are in the [Reference](#reference) entry.
- [`BaseProcessEntryTask`](#baseprocessentrytask) — validates individual keys, creates/refreshes Django entries, and chains next-level/missing-issue tasks; see the [Reference](#reference) entry.
- [`BaseComicvineInfoTask`](#basecomicvineinfotask) — refreshes individual records from Comicvine and retries on failure; refer to the [Reference](#reference) entry.
- [`BaseRefreshTask`](#baserefreshtask) — refreshes stale records by comparing Mongo crawl timestamps; details in the [Reference](#reference) entry.
- [`full_increment_update`](#full_increment_update) — shared Scrapy task that runs the incremental `FullSpider` job; see the [Reference](#reference) entry.
- [`full_skip_existing_increment_update`](#full_skip_existing_increment_update) — similar to `full_increment_update` but skips already indexed items.
- [`full_skip_existing_update`](#full_skip_existing_update) — runs a non-incremental crawl but skips existing data.
- [`full_update`](#full_update) — runs a full crawl without skipping existing entries.

## Reference

### `WrongKeyFormatError`
- Raised by `BaseProcessEntryTask` when a storage key does not match the expected regular expression.

### `BaseSpaceTask`
- Abstract Celery `Task` that scans a DigitalOcean Space prefix and queues entry-level tasks for unprocessed objects.

#### Class attributes
- `PROCESS_ENTRY_TASK`: Task class to invoke for each unprocessed key.
- `LOGGER_NAME`: Logger name used to instantiate the task logger.
- `priority`: Default Celery priority for the task (9).

#### Methods
- `get_processed_keys(self)`
  - Returns the already processed key list (defaults to an empty list; override if you track state outside of S3).
- `run(self, *args, **kwargs)`
  - `kwargs['prefix']`: Space prefix to scan.
  - Optional `parent_entry_id`: passed to child tasks.
  - Loads objects under the prefix, filters them with `_regexp`, and enqueues `PROCESS_ENTRY_TASK` for every unprocessed key, passing along the `size` and `parent_entry_id`.
- `__init__(self)`
  - Instantiates the S3 client/space bucket, compiles `_regexp` for key filtering, and sets `_logger` plus containers for results.

### `BaseProcessEntryTask`
- Task that validates individual file keys, creates or refreshes the corresponding model entry, and optionally queues next-level or missing-issue tasks.

#### Class attributes
- `NEXT_LEVEL_TASK`: Task triggered after an entry is created, given the same prefix.
- `MODEL_NAME`, `APP_LABEL`: Target Django model to load via `apps.get_model`.
- `LOGGER_NAME`: Logger name used for structured logging.
- `PARENT_ENTRY_*`: Attributes that define a parent relation (model/app/field) when nesting tasks.
- `MISSING_ISSUES_TASK`: Optional task to notify missing issue watchers.
- Retry settings: `autoretry_for`, `retry_kwargs`, `retry_backoff`, `retry_backoff_max`, `priority`.

#### Methods
- `check_key_format(self, key)`
  - Ensures `key` matches `_key_regexp` (compiled in `__init__`).
- `get_defaults(self, **kwargs)`
  - When `parent_entry` information is provided, loads the parent model and returns defaults mapping `PARENT_ENTRY_FIELD` to the parent instance.
- `get_comicvine_id(self, key)`
  - Parses the Comicvine ID from `key` using `_id_regexp`.
- `run(self, *args, **kwargs)`
  - `key`: Required S3 key.
  - `parent_entry_id`: Optional, forwarded to `get_defaults`.
  - After validation, gets/creates the model via `get_or_create_from_comicvine(force_refresh=True)`.
  - Optionally triggers `MISSING_ISSUES_TASK`, then queues `NEXT_LEVEL_TASK` with the current prefix and new entry ID.
- `__init__(self)`
  - Compiles `_id_regexp` for parsing IDs and sets up `_logger`.

### `BaseComicvineInfoTask`
- Task that keeps individual entries up to date by calling `fill_from_comicvine`, retries on DB/operational errors, and marks the record as not matched on failure.

#### Attributes
- `MODEL_NAME`, `APP_LABEL`: Target model.
- Retry settings for Celery (autoretry/backoff) and optional `MISSING_ISSUES_TASK`.

#### Methods
- `run(self, *args, **kwargs)`
  - `pk`: Primary key of the record to refresh.
  - Forwards `kwargs` (e.g., `force_api_refresh`) to `obj.fill_from_comicvine`, saves the object, and enqueues `MISSING_ISSUES_TASK` when watchers/issues exist.
- `_set_not_matched(self, kwargs)`
  - Sets the record status to `NOT_MATCHED` if it is not already matched; used by failure handlers.
- `on_failure(self, exc, task_id, args, kwargs, einfo)`
  - Calls `_set_not_matched` after a failure.
- `on_retry(self, exc, task_id, args, kwargs, einfo)`
  - Also marks the record as not matched when Celery retries.

### `BaseRefreshTask`
- Task that sequentially compares Comicvine crawl timestamps (from Mongo) to local `comicvine_last_match` values and schedules delayed `fill_from_comicvine` jobs for stale records.

#### Methods
- `run(self, *args, **kwargs)`
  - Loads all objects that are not `QUEUED`, fetches their Comicvine IDs, reads the corresponding documents from Mongo, and re-queues any objects whose local `comicvine_last_match` is missing or older than the Mongo `crawl_date`.

### `full_increment_update`
- Shared Celery task that instantiates a Scrapy `FullSpider` job, configured via `read_comics.spiders.settings`, and runs it through the `Processor` helper (incremental mode only).

### `full_skip_existing_increment_update`
- Shared Celery task that runs `FullSpider` incrementally but skips already indexed items (`skip_existing="Y"`).

### `full_skip_existing_update`
- Shared Celery task that runs a non-incremental `FullSpider` crawl while skipping existing items.

### `full_update`
- Shared Celery task that executes a complete `FullSpider` crawl without skipping any entries (`incremental="N"`, `skip_existing="N"`).
