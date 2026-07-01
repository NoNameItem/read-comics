# Tasks defined in `characters/tasks.py`

## Summary

- [`CharacterComicvineInfoTask`](#charactercomicvineinfotask) — refreshes individual character records from ComicVine and queues missing issues tasks; see the [Reference](#reference) entry for configuration.
- [`character_comicvine_info_task`](#character_comicvine_info_task) — registered Celery task instance for character synchronization.
- [`CharactersRefreshTask`](#charactersrefreshtask) — scans all characters comparing MongoDB crawl timestamps to local data and re-queues stale records; details in the [Reference](#reference) entry.
- [`characters_refresh_task`](#characters_refresh_task) — registered Celery task instance for batch character refresh.
- [`characters_increment_update`](#characters_increment_update) — runs incremental ComicVine spider to fetch new/updated characters.
- [`characters_skip_existing_increment_update`](#characters_skip_existing_increment_update) — incremental spider that skips already indexed characters.
- [`characters_skip_existing_update`](#characters_skip_existing_update) — full spider crawl that skips existing characters.
- [`characters_update`](#characters_update) — complete spider crawl fetching all characters without skipping.

## Reference

### `CharacterComicvineInfoTask`

- Celery task class that inherits from [`BaseComicvineInfoTask`](../utils/tasks.md#basecomicvineinfotask).
- Synchronizes individual [`Character`](models.md#character) records by calling `fill_from_comicvine` with retry logic on database errors.
- Queues missing issues task after successful synchronization to notify watchers.

#### Class attributes

- `MODEL_NAME = "Character"`: Django model name to synchronize.
- `APP_LABEL = "characters"`: Django app label containing the model.
- `MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.CharacterMissingIssuesTask"`: Task path for notifying watchers about character updates.

#### Inherited behavior

- Inherits retry configuration, error handling, and core synchronization logic from [`BaseComicvineInfoTask`](../utils/tasks.md#basecomicvineinfotask).
- Automatically retries on `DatabaseError` and `OperationalError`.
- Marks records as `NOT_MATCHED` on permanent failure.
- See [`BaseComicvineInfoTask`](../utils/tasks.md#basecomicvineinfotask) for detailed method documentation.

### `character_comicvine_info_task`

- Registered Celery task instance created from `CharacterComicvineInfoTask`.
- Registered with the main Celery app via `celery_app.register_task()`.
- Referenced in [`Character.COMICVINE_INFO_TASK`](models.md#character) for deferred synchronization.

#### Usage

```python
# Queue character synchronization by primary key
character_comicvine_info_task.delay(pk=123)

# Force API refresh (bypass MongoDB cache)
character_comicvine_info_task.delay(pk=123, force_api_refresh=True)
```

### `CharactersRefreshTask`

- Celery task class that inherits from [`BaseRefreshTask`](../utils/tasks.md#baserefreshtask).
- Scans all [`Character`](models.md#character) records that are not in `QUEUED` status.
- Compares local `comicvine_last_match` timestamps with MongoDB `crawl_date` values.
- Queues `character_comicvine_info_task` for characters with stale data.

#### Class attributes

- `MODEL_NAME = "Character"`: Django model name to refresh.
- `APP_LABEL = "characters"`: Django app label containing the model.

#### Inherited behavior

- Inherits MongoDB integration and timestamp comparison logic from [`BaseRefreshTask`](../utils/tasks.md#baserefreshtask).
- Loads character ComicVine IDs, fetches corresponding MongoDB documents, and schedules refresh tasks.
- See [`BaseRefreshTask`](../utils/tasks.md#baserefreshtask) for detailed method documentation.

### `characters_refresh_task`

- Registered Celery task instance created from `CharactersRefreshTask`.
- Registered with the main Celery app via `celery_app.register_task()`.

#### Usage

```python
# Queue batch refresh of all stale characters
characters_refresh_task.delay()
```

### `characters_increment_update`

- Shared Celery task decorated with `@shared_task`.
- Runs incremental ComicVine spider to fetch new and updated characters.
- Uses `CharactersSpider` with configuration: `incremental="Y"`, `skip_existing="N"`.

#### Behavior

- Initializes Scrapy settings from `read_comics.spiders.settings`.
- Creates `Processor` instance with spider settings.
- Creates `Job` for `CharactersSpider` in incremental mode.
- Executes spider job synchronously via `Processor.run()`.
- Fetches characters added/updated since last crawl timestamp.
- Re-processes existing characters even if already indexed.

#### Parameters

- None (task takes no arguments).

#### Returns

- `None`

### `characters_skip_existing_increment_update`

- Shared Celery task decorated with `@shared_task`.
- Runs incremental ComicVine spider while skipping already indexed characters.
- Uses `CharactersSpider` with configuration: `incremental="Y"`, `skip_existing="Y"`.

#### Behavior

- Identical to `characters_increment_update` but skips characters already present in MongoDB.
- More efficient when most characters are already indexed.
- Only processes new characters added since last crawl.

#### Parameters

- None (task takes no arguments).

#### Returns

- `None`

### `characters_skip_existing_update`

- Shared Celery task decorated with `@shared_task`.
- Runs full ComicVine spider crawl while skipping existing characters.
- Uses `CharactersSpider` with configuration: `incremental="N"`, `skip_existing="Y"`.

#### Behavior

- Crawls entire ComicVine character catalog from beginning.
- Skips characters already present in MongoDB.
- Useful for filling gaps in collection without re-processing existing data.

#### Parameters

- None (task takes no arguments).

#### Returns

- `None`

### `characters_update`

- Shared Celery task decorated with `@shared_task`.
- Runs complete ComicVine spider crawl without any filtering.
- Uses `CharactersSpider` with configuration: `incremental="N"`, `skip_existing="N"`.

#### Behavior

- Crawls entire ComicVine character catalog from beginning.
- Re-processes all characters regardless of existing MongoDB data.
- Most resource-intensive option but ensures complete data refresh.
- Useful for full re-sync or recovery scenarios.

#### Parameters

- None (task takes no arguments).

#### Returns

- `None`

## Task routing

All tasks in this module are automatically routed based on naming patterns configured in [`config/celery_app.py`](../../config/celery_app.md):

- Tasks ending with `_update` → routed to `read_comics_spiders` queue (Scrapy crawlers)
- `CharacterComicvineInfoTask` → routed to `read_comics_default` queue (general processing)
- `CharactersRefreshTask` → routed to `read_comics_default` queue (general processing)

## Common usage patterns

### Synchronize single character

```python
from read_comics.characters.tasks import character_comicvine_info_task

# By primary key
character_comicvine_info_task.delay(pk=123)

# Force fresh API call
character_comicvine_info_task.delay(pk=123, force_api_refresh=True)
```

### Refresh all stale characters

```python
from read_comics.characters.tasks import characters_refresh_task

# Queue batch refresh
characters_refresh_task.delay()
```

### Run spider crawls

```python
from read_comics.characters.tasks import (
    characters_increment_update,
    characters_skip_existing_increment_update,
    characters_skip_existing_update,
    characters_update
)

# Incremental crawl (new/updated characters only)
characters_increment_update.delay()

# Incremental crawl skipping indexed characters (most efficient)
characters_skip_existing_increment_update.delay()

# Full crawl skipping indexed characters
characters_skip_existing_update.delay()

# Complete re-crawl (everything)
characters_update.delay()
```
