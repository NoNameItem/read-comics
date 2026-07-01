# Volumes Celery Tasks

## Summary

- `VolumeProcessEntryTask` — Processes DigitalOcean Spaces directory entries for new volumes
- `VolumesSpaceTask` — Lists and filters S3 volume directories for processing
- `VolumeComicvineInfoTask` — Syncs volume data from MongoDB to PostgreSQL
- `VolumesRefreshTask` — Full refresh of all volumes from scratch
- 4 spider tasks — Different sync strategies (incremental, skip_existing combinations)

## Reference

### VolumeProcessEntryTask

Base task for processing S3 volume directories and creating/updating Volume records.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `MODEL_NAME` | `"Volume"` | Django model class name |
| `APP_LABEL` | `"volumes"` | Django app for model lookup |
| `LOGGER_NAME` | `"VolumeProcessEntryTask"` | Logger identifier |
| `PARENT_ENTRY_MODEL_NAME` | `"Publisher"` | Parent entity (Publisher owns Volumes) |
| `PARENT_ENTRY_APP_LABEL` | `"publishers"` | Parent entity app |
| `PARENT_ENTRY_FIELD` | `"publisher"` | Foreign key field name |
| `NEXT_LEVEL_TASK` | `issues_space_task` | Task to call after processing volume |
| `MISSING_ISSUES_TASK` | `"read_comics.missing_issues.tasks.VolumeMissingIssuesTask"` | Missing issues detection task |

#### Key Regexp

```python
_key_regexp = re.compile(r"^.* \[\d\d\d\d\] \[\d+\]\/$")
```

Matches volume directories with pattern: `Name [YYYY] [ID]/`
- `Name` — Volume/series name (anything)
- `[YYYY]` — 4-digit year in brackets
- `[ID]` — Numeric ID in brackets
- `/` — Directory indicator

---

### VolumesSpaceTask

Task for listing S3 volume directories and filtering already-processed ones.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `PROCESS_ENTRY_TASK` | `volume_entry_task` | Task to call for each new volume |
| `LOGGER_NAME` | `"read_comics.tasks.VolumesSpaceTask"` | Logger identifier |

#### get_processed_keys() Logic

Queries for processed volume directories:
1. Gets all Issue.space_key values (already processed issues)
2. For each volume, checks if child issues exist in space
3. Returns volumes that have ALL their issues processed
4. Removes processed volumes from queue to avoid re-processing

#### Behavior

- Lists volume directories from S3
- Filters out volumes with unprocessed issues
- Queues only volumes ready for completion

---

### VolumeComicvineInfoTask

Base Celery task for syncing volume data from MongoDB to PostgreSQL.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `MODEL_NAME` | `"Volume"` | Django model class name |
| `APP_LABEL` | `"volumes"` | Django app for model lookup |
| `MISSING_ISSUES_TASK` | `"read_comics.missing_issues.tasks.VolumeMissingIssuesTask"` | Task to trigger missing issues detection |

#### Behavior

Inherited from `BaseComicvineInfoTask`:
- Retrieves MongoDB document by ID
- Applies field mapping and transformations
- Resolves FK references (publisher, first_issue, last_issue)
- Creates or updates PostgreSQL Volume record
- Triggers missing issues detection

---

### VolumesRefreshTask

Full refresh task for all volumes (re-fetch all data from ComicVine).

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `MODEL_NAME` | `"Volume"` | Django model class name |
| `APP_LABEL` | `"volumes"` | Django app for model lookup |

#### Behavior

Inherited from `BaseRefreshTask`:
- Queues all volume IDs for re-fetching
- Executes spider with `incremental=False`
- Replaces existing data with fresh ComicVine data

---

### Spider Tasks (4 variants)

Four Celery tasks with different sync strategies:

| Task Name | Config | Behavior | Schedule |
|---|---|---|---|
| `volumes_increment_update()` | incr=Y, skip=N | Modified volumes, full data | Every 6-12 hours |
| `volumes_skip_existing_increment_update()` | incr=Y, skip=Y | Modified volumes, skip cached detail | Every 12-24 hours |
| `volumes_skip_existing_update()` | incr=N, skip=Y | All volumes, skip cached detail | As-needed |
| `volumes_update()` | incr=N, skip=N | All volumes, full refresh | Weekly/monthly |

#### Parameters

- **incremental="Y"** — Uses `date_last_updated` filter to fetch only modified volumes
- **incremental="N"** — Fetches all volumes regardless of modification date
- **skip_existing="Y"** — Skips detail requests if `crawl_source="detail"` already set
- **skip_existing="N"** — Fetches all detail data even if cached

---

## Task Execution Flow

1. **Spider Execution** — VolumesSpider fetches from ComicVine API
2. **MongoDB Storage** — MongoPipeline stores JSON in `comicvine_volumes` collection
3. **Celery Task Trigger** — MongoPipeline triggers VolumeComicvineInfoTask
4. **PostgreSQL Sync** — Field mapping applied, FKs resolved, Volume record created/updated
5. **Post-Save Cleanup** — Deletes IgnoredVolume/IgnoredIssue records
6. **Missing Issues** — VolumeMissingIssuesTask queued to detect gaps
7. **Space Processing** — VolumeProcessEntryTask processes S3 directories

## References

- [../models.md](../models.md) — Volume model definition with field mapping
- [../spiders/volumes_spider.md](../spiders/volumes_spider.md) — VolumesSpider configuration
- [../../utils/tasks.md](../../utils/tasks.md) — BaseComicvineInfoTask, BaseRefreshTask, BaseProcessEntryTask, BaseSpaceTask
- [../../missing_issues/tasks.md](../../missing_issues/tasks.md) — VolumeMissingIssuesTask
- [../../issues/tasks.md](../../issues/tasks.md) — issues_space_task for issue processing