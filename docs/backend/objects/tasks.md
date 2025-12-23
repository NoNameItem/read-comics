# Objects Tasks

## Summary

- [`ObjectComicvineInfoTask`](#objectcomicvineinfotask) — Syncs individual object data from ComicVine API
- [`ObjectsRefreshTask`](#objectsrefreshtask) — Batch refresh of all objects from ComicVine
- Spider tasks — Scrapy-based crawling with incremental and skip options

## Reference

### `ObjectComicvineInfoTask`

Syncs individual object data from ComicVine API using FIELD_MAPPING and automatic conversion methods.

**Inheritance:** `BaseComicvineInfoTask`

**Configuration:**

- `MODEL_NAME = "Object"` — Target model
- `APP_LABEL = "objects"` — Django app name
- `MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.ObjectMissingIssuesTask"` — Task to queue missing issues

**Behavior:**

Inherited from `BaseComicvineInfoTask`:
1. Fetches object data from ComicVine API endpoint
2. Maps ComicVine fields to Django fields using FIELD_MAPPING
3. Handles `first_issue_comicvine_id` → `first_issue` FK resolution
4. Creates/updates Object record
5. Queues ObjectMissingIssuesTask for missing issue tracking
6. Sets `comicvine_status` to MATCHED
7. Updates `comicvine_last_match` timestamp

---

### `ObjectsRefreshTask`

Batch refresh task to update all objects from ComicVine API.

**Inheritance:** `BaseRefreshTask`

**Configuration:**

- `MODEL_NAME = "Object"` — Target model
- `APP_LABEL = "objects"` — Django app name

**Behavior:**

Iterates over Object records and queues ObjectComicvineInfoTask for each. Keeps all object data synchronized with ComicVine.

---

### Spider Tasks

Scrapy-based crawling tasks for Objects with different update strategies.

#### `objects_increment_update()`

Incremental update: fetches only new objects since last crawl.

- `incremental="Y"` — Only new items
- `skip_existing="N"` — Process all items in response

**Use case:** Regular updates for new objects (faster, lower API quota usage)

#### `objects_skip_existing_increment_update()`

Incremental update with deduplication: skips objects already imported.

- `incremental="Y"` — Only new items
- `skip_existing="Y"` — Skip already-imported items

**Use case:** Most efficient option for regular crawls

#### `objects_skip_existing_update()`

Full update, skipping already-imported objects in result set.

- `incremental="N"` — All items
- `skip_existing="Y"` — Skip already-imported

**Use case:** Complete refresh with import prevention

#### `objects_update()`

Full recrawl without skipping.

- `incremental="N"` — All items
- `skip_existing="N"` — Reimport everything

**Use case:** Recovery/maintenance, slowest (highest API usage)
