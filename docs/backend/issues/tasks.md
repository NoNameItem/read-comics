# Issues Tasks

## Summary

- [`IssueProcessEntryTask`](#issueprocessentrytask) — Processes digital file entries from DigitalOcean Space
- [`IssuesSpaceTask`](#issuesspacetask) — Scans DigitalOcean Space for new files to process
- [`IssueComicvineInfoTask`](#issuecomicvineinfotask) — Syncs individual issue data from ComicVine API
- [`IssuesRefreshTask`](#issuesrefreshtask) — Batch refresh of all issues from ComicVine
- [`purge_deleted()`](#purge_deleted) — Removes orphaned Issue records for deleted files
- Spider tasks — Scrapy-based crawling with incremental and skip options

## Reference

### `IssueProcessEntryTask`

Processes individual file entries from DigitalOcean Space and creates/updates Issue records.

**Inheritance:** `BaseProcessEntryTask`

**Configuration:**

- `MODEL_NAME = "Issue"` — Target model
- `APP_LABEL = "issues"` — Django app name
- `LOGGER_NAME = "IssueProcessEntryTask"` — Logger identifier
- `PARENT_ENTRY_MODEL_NAME = "Volume"` — Issues belong to Volumes
- `PARENT_ENTRY_APP_LABEL = "volumes"` — Volume app
- `PARENT_ENTRY_FIELD = "volume"` — FK field name

**File Validation:**

- Regex validates filenames like: `"Volume Name #42 [12345].cbr"` (Comic Book archive format)

**Methods:**

- `get_defaults(kwargs)` — Extracts `space_key` (file path) and `size` (bytes) for Issue creation

---

### `IssuesSpaceTask`

Scans DigitalOcean Space bucket for issue files and triggers processing for new files.

**Inheritance:** `BaseSpaceTask`

**Configuration:**

- `PROCESS_ENTRY_TASK = issue_entry_task` — Task to run for each new file
- `LOGGER_NAME = "IssuesSpaceTask"` — Logger identifier

**Methods:**

- `get_processed_keys()` → Returns set of all `space_key` values for MATCHED issues. Used to skip already-processed files.

---

### `IssueComicvineInfoTask`

Syncs individual issue data from ComicVine API using FIELD_MAPPING and automatic conversion methods.

**Inheritance:** `BaseComicvineInfoTask`

**Configuration:**

- `MODEL_NAME = "Issue"` — Target model
- `APP_LABEL = "issues"` — Django app name

**Behavior:**

Inherited from `BaseComicvineInfoTask`:
1. Fetches issue data from ComicVine API endpoint
2. Maps ComicVine fields to Django fields using FIELD_MAPPING
3. Handles conversion methods for dates, relationships, variant covers
4. Creates/updates Issue record
5. Sets `comicvine_status` to MATCHED
6. Updates `comicvine_last_match` timestamp

---

### `IssuesRefreshTask`

Batch refresh task to update all issues from ComicVine API.

**Inheritance:** `BaseRefreshTask`

**Configuration:**

- `MODEL_NAME = "Issue"` — Target model
- `APP_LABEL = "issues"` — Django app name

**Behavior:**

Iterates over Issue records and queues IssueComicvineInfoTask for each. Keeps all issue data synchronized with ComicVine.

---

### Spider Tasks

Scrapy-based crawling tasks for Issues with different update strategies.

#### `issues_increment_update()`

Incremental update: fetches only new issues since last crawl.

- `incremental="Y"` — Only new items
- `skip_existing="N"` — Process all items in response

**Use case:** Regular updates for new releases (faster, lower API quota usage)

#### `issues_skip_existing_increment_update()`

Incremental update with deduplication: skips issues already imported.

- `incremental="Y"` — Only new items
- `skip_existing="Y"` — Skip already-imported items

**Use case:** Most efficient option for regular crawls

#### `issues_skip_existing_update()`

Full update, skipping already-imported issues in result set.

- `incremental="N"` — All items
- `skip_existing="Y"` — Skip already-imported

**Use case:** Complete refresh with import prevention

#### `issues_update()`

Full recrawl without skipping.

- `incremental="N"` — All items
- `skip_existing="N"` — Reimport everything

**Use case:** Recovery/maintenance, slowest (highest API usage)

---

### `purge_deleted()`

Removes Issue records for deleted files in DigitalOcean Space.

**Process:**

1. Connects to DigitalOcean Space S3 via boto3
2. Fetches list of all files in bucket
3. Deletes Issue records whose `space_key` not in bucket

**Use case:** Cleanup task to prevent orphaned Issue records.
