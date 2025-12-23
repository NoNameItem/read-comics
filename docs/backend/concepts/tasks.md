# Concept Tasks

Celery tasks for syncing concept data from ComicVine API and refreshing the database.

## Summary

- [`ConceptComicvineInfoTask`](#conceptcomicvineinfotask) — Syncs individual concept data from ComicVine
- [`ConceptsRefreshTask`](#conceptsrefreshtask) — Batch refresh of all concept data
- [`concepts_increment_update()`](#concepts_increment_update) — Incremental spider update (skip missing)
- [`concepts_skip_existing_increment_update()`](#concepts_skip_existing_increment_update) — Incremental with skip existing
- [`concepts_skip_existing_update()`](#concepts_skip_existing_update) — Full refresh with skip existing
- [`concepts_update()`](#concepts_update) — Full refresh of all concepts

## Reference

### `ConceptComicvineInfoTask`

**Base Class:** `BaseComicvineInfoTask`

**Configuration:**

| Property | Value | Purpose |
|----------|-------|---------|
| `MODEL_NAME` | `"Concept"` | Model class name for targeting |
| `APP_LABEL` | `"concepts"` | Django app label |
| `MISSING_ISSUES_TASK` | `"read_comics.missing_issues.tasks.ConceptMissingIssuesTask"` | Task to run after sync for missing issues |

**Task:** `concept_comicvine_info_task`

Syncs a single concept's ComicVine data. Called by the model's `sync_with_comicvine()` method when a concept is created or updated.

**Behavior:**

- Fetches data from ComicVine API using concept's comicvine_id
- Updates local model fields: name, aliases, description, image URLs, start_year
- Resolves first_issue_comicvine_id to Issue FK reference
- Sets comicvine_status to "synced" on success, "failed" on error
- Triggers ConceptMissingIssuesTask to update missing issues tracking

**Example Usage:**

```python
from read_comics.concepts.models import Concept
from read_comics.concepts.tasks import concept_comicvine_info_task

concept = Concept.objects.get(comicvine_id=75632)
concept_comicvine_info_task.delay(concept.id)  # Async execution
```

---

### `ConceptsRefreshTask`

**Base Class:** `BaseRefreshTask`

**Configuration:**

| Property | Value | Purpose |
|----------|-------|---------|
| `MODEL_NAME` | `"Concept"` | Model class name |
| `APP_LABEL` | `"concepts"` | Django app label |

**Task:** `concepts_refresh_task`

Batch refresh task that updates all concepts in the database. Called periodically via Celery Beat.

**Behavior:**

- Iterates all Concept records
- Calls sync_with_comicvine() for each to update from API
- Handles failures gracefully (continues on errors)
- Reports summary of synced vs failed concepts

---

### `concepts_increment_update()`

**Type:** `@shared_task`

Incremental spider update that only fetches new concept data, skipping already-synced concepts.

**Configuration:**

- `incremental="Y"` — Only fetch new/recently modified concepts
- `skip_existing="N"` — Re-sync concepts that already exist

**Schedule:** Usually run hourly via Celery Beat to catch new concepts

**Usage:**

```python
from read_comics.concepts.tasks import concepts_increment_update

concepts_increment_update.delay()  # Run in background
```

---

### `concepts_skip_existing_increment_update()`

**Type:** `@shared_task`

Incremental spider update that fetches new concepts but skips any that already exist in database.

**Configuration:**

- `incremental="Y"` — Only fetch new/recently modified
- `skip_existing="Y"` — Skip concepts already in database

**Schedule:** Useful for reducing API calls when running frequently

**Usage:**

```python
from read_comics.concepts.tasks import concepts_skip_existing_increment_update

concepts_skip_existing_increment_update.delay()
```

---

### `concepts_skip_existing_update()`

**Type:** `@shared_task`

Full refresh that fetches all concept data but skips those already synced in database.

**Configuration:**

- `incremental="N"` — Fetch all concepts from API
- `skip_existing="Y"` — Skip already-existing concepts

**Schedule:** Run daily or weekly for comprehensive refresh while avoiding duplicate API calls

**Usage:**

```python
from read_comics.concepts.tasks import concepts_skip_existing_update

concepts_skip_existing_update.delay()
```

---

### `concepts_update()`

**Type:** `@shared_task`

Full refresh of all concept data. Re-syncs everything including already-existing concepts.

**Configuration:**

- `incremental="N"` — Fetch all concepts from API
- `skip_existing="N"` — Re-sync even already-existing concepts

**Schedule:** Run on demand or monthly for complete database refresh

**Usage:**

```python
from read_comics.concepts.tasks import concepts_update

concepts_update.delay()
```

---

## Spider Configuration

All spider tasks use:

- **Spider Class:** `ConceptsSpider` from `spiders.spiders.concepts_spider`
- **Processor:** `Processor` wrapper for Scrapy job execution
- **Settings:** Django Scrapy integration via `read_comics.spiders.settings`

**Common Parameters:**

- `incremental` — `"Y"` (fetch only new) or `"N"` (fetch all)
- `skip_existing` — `"Y"` (skip if in DB) or `"N"` (re-sync all)

## Routing

All tasks are routed to appropriate Celery queues based on priority and type via Celery configuration.