# Story Arcs Celery Tasks

## Summary

- `StoryArcComicvineInfoTask` — Syncs story arc data from MongoDB to PostgreSQL
- `StoryArcsRefreshTask` — Full refresh of all story arcs from scratch
- 4 spider tasks — Different sync strategies (incremental, skip_existing combinations)

## Reference

### StoryArcComicvineInfoTask

Base Celery task for syncing story arc data from MongoDB cache to PostgreSQL database.

Inherits from `BaseComicvineInfoTask` which handles:
- MongoDB document retrieval
- Field mapping and transformation
- FK resolution (publisher, first_issue)
- Model creation/update

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `MODEL_NAME` | `"StoryArc"` | Django model class name |
| `APP_LABEL` | `"story_arcs"` | Django app for model lookup |
| `MISSING_ISSUES_TASK` | `"read_comics.missing_issues.tasks.StoryArcMissingIssuesTask"` | Task to trigger missing issues detection after sync |

#### Task Instance

```python
story_arc_comicvine_info_task = celery_app.register_task(StoryArcComicvineInfoTask())
```

#### Execution

Called automatically by spider pipeline after storing data in MongoDB:
1. MongoDB document created/updated
2. Task triggered with document ID
3. Field mapping applied
4. ForeignKey references resolved
5. PostgreSQL record created/updated
6. Missing issues task queued for related story arcs

---

### StoryArcsRefreshTask

Full refresh task for all story arcs (re-fetch all data from ComicVine).

Inherits from `BaseRefreshTask` which handles:
- Batch processing all entities
- Task queuing via spider execution
- Error handling and retries

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `MODEL_NAME` | `"StoryArc"` | Django model class name |
| `APP_LABEL` | `"story_arcs"` | Django app for model lookup |

#### Task Instance

```python
story_arcs_refresh_task = celery_app.register_task(StoryArcsRefreshTask())
```

#### Execution

Manual task for periodic full refreshes:
- Queues all story arc IDs for re-fetching
- Executes spider with `incremental=False`
- Replaces existing data with fresh ComicVine data

---

### Spider Tasks (4 variants)

Four Celery tasks with different sync strategies:

#### 1. story_arcs_increment_update()

**Configuration**: `incremental="Y"`, `skip_existing="N"`

**Behavior**:
- Fetches only story arcs modified since last run
- Re-fetches all data including detail views
- Useful for regular incremental updates

**Typical schedule**: Every 6-12 hours

---

#### 2. story_arcs_skip_existing_increment_update()

**Configuration**: `incremental="Y"`, `skip_existing="Y"`

**Behavior**:
- Fetches only modified story arcs
- Skips detail fetches for story arcs already cached with complete data
- Saves API calls for unchanged data

**Typical schedule**: Every 12-24 hours (most efficient)

---

#### 3. story_arcs_skip_existing_update()

**Configuration**: `incremental="N"`, `skip_existing="Y"`

**Behavior**:
- Full fetch of all story arcs
- Skips detail requests for already-cached story arcs
- Useful after resuming from downtime

**Typical schedule**: As-needed (e.g., after maintenance)

---

#### 4. story_arcs_update()

**Configuration**: `incremental="N"`, `skip_existing="N"`

**Behavior**:
- Full re-fetch of all story arcs
- Fetches all detail data even if cached
- Complete data refresh, highest API usage

**Typical schedule**: Weekly or monthly (resource intensive)

---

## Implementation Details

### Task Structure

All spider tasks follow same pattern:

```python
@shared_task
def story_arcs_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(StoryArcsSpider, incremental="Y", skip_existing="N")
    p.run(j)
```

1. Load Scrapy settings from spiders_settings_file
2. Create Processor (runs spider in subprocess)
3. Create Job with StoryArcsSpider and sync parameters
4. Execute processor with job

### Parameters Explained

- **incremental="Y"** — Use `date_last_updated` filter to fetch only modified entities
- **incremental="N"** — Fetch all entities regardless of modification date
- **skip_existing="Y"** — Middleware skips detail requests if `crawl_source="detail"` already set
- **skip_existing="N"** — Fetch all detail data even if already cached

### Data Flow

Spider tasks → MongoDB storage → StoryArcComicvineInfoTask → PostgreSQL → Missing issues detection

## References

- [../models.md](../models.md) — StoryArc model definition
- [../spiders/story_arcs_spider.md](../spiders/story_arcs_spider.md) — StoryArcsSpider configuration
- [../../utils/tasks.md](../../utils/tasks.md) — BaseComicvineInfoTask and BaseRefreshTask