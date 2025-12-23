# Locations Tasks

## Summary

- [`LocationComicvineInfoTask`](#locationcomicvineinfotask) — Syncs individual location data from ComicVine API
- [`LocationsRefreshTask`](#locationsrefreshtask) — Batch refresh of all locations from ComicVine
- Spider tasks — Scrapy-based crawling with incremental and skip options

## Reference

### `LocationComicvineInfoTask`

Syncs individual location data from ComicVine API using FIELD_MAPPING and automatic conversion methods.

**Inheritance:** `BaseComicvineInfoTask`

**Configuration:**

- `MODEL_NAME = "Location"` — Target model
- `APP_LABEL = "locations"` — Django app name
- `MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.LocationMissingIssuesTask"` — Task to queue missing issues

**Behavior:**

Inherited from `BaseComicvineInfoTask`:
1. Fetches location data from ComicVine API endpoint
2. Maps ComicVine fields to Django fields using FIELD_MAPPING
3. Handles `first_issue_comicvine_id` → `first_issue` FK resolution
4. Creates/updates Location record
5. Queues LocationMissingIssuesTask for missing issue tracking
6. Sets `comicvine_status` to MATCHED
7. Updates `comicvine_last_match` timestamp

---

### `LocationsRefreshTask`

Batch refresh task to update all locations from ComicVine API.

**Inheritance:** `BaseRefreshTask`

**Configuration:**

- `MODEL_NAME = "Location"` — Target model
- `APP_LABEL = "locations"` — Django app name

**Behavior:**

Iterates over Location records and queues LocationComicvineInfoTask for each. Keeps all location data synchronized with ComicVine.

---

### Spider Tasks

Scrapy-based crawling tasks for Locations with different update strategies.

#### `locations_increment_update()`

Incremental update: fetches only new locations since last crawl.

- `incremental="Y"` — Only new items
- `skip_existing="N"` — Process all items in response

**Use case:** Regular updates for new locations (faster, lower API quota usage)

#### `locations_skip_existing_increment_update()`

Incremental update with deduplication: skips locations already imported.

- `incremental="Y"` — Only new items
- `skip_existing="Y"` — Skip already-imported items

**Use case:** Most efficient option for regular crawls

#### `locations_skip_existing_update()`

Full update, skipping already-imported locations in result set.

- `incremental="N"` — All items
- `skip_existing="Y"` — Skip already-imported

**Use case:** Complete refresh with import prevention

#### `locations_update()`

Full recrawl without skipping.

- `incremental="N"` — All items
- `skip_existing="N"` — Reimport everything

**Use case:** Recovery/maintenance, slowest (highest API usage)
