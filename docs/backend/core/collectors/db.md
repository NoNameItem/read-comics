# Database Collector

Prometheus metrics collector for PostgreSQL database statistics.

## Summary

- [`DBCollector`](#dbcollector) — Collects metrics on database record counts by sync status and model

## Reference

### `DBCollector`

Collects database metrics on record counts for each model, broken down by ComicVine sync status.

**Base Class:** [`BaseCollector`](base.md#basecollector)

**Tracked Models:**

```python
MODELS = {
    "characters": Character,
    "concepts": Concept,
    "issues": Issue,
    "locations": Location,
    "objects": Object,
    "people": Person,
    "powers": Power,
    "publishers": Publisher,
    "story_arcs": StoryArc,
    "teams": Team,
    "volumes": Volume,
}
```

**Metrics Registered:**

- `read_comics_db_count` (Gauge, "Number of rows in database")
  - Labels:
    - `table` (string): Model name or "total"
    - `status` (string): ComicVine sync status
  - Statuses:
    - `"all"` — Total records in table
    - `"matched"` — Records synced from ComicVine (MATCHED status)
    - `"not_matched"` — Records not yet matched (NOT_MATCHED status)
    - `"queued"` — Records in API sync queue (QUEUED status)

**Behavior:**

- For each model in MODELS:
  - Queries database for record counts grouped by `comicvine_status`
  - Sets metric values for each status breakdown
  - Increments running totals under `table="total"`
- Aggregates across all models for overall database statistics
- Uses Django ORM `Count` aggregation for efficient queries

**Example Output (Prometheus format):**

```
# HELP read_comics_db_count Number of rows in database
# TYPE read_comics_db_count gauge
read_comics_db_count{status="all",table="characters"} 1250
read_comics_db_count{status="matched",table="characters"} 1200
read_comics_db_count{status="not_matched",table="characters"} 50
read_comics_db_count{status="queued",table="characters"} 0
read_comics_db_count{status="all",table="issues"} 85000
read_comics_db_count{status="matched",table="issues"} 84500
...
read_comics_db_count{status="all",table="total"} 500000
read_comics_db_count{status="matched",table="total"} 495000
read_comics_db_count{status="not_matched",table="total"} 4500
read_comics_db_count{status="queued",table="total"} 500
```

**Sync Status Meanings:**

- **MATCHED** — Record successfully synced from ComicVine API
- **NOT_MATCHED** — Record not yet matched to ComicVine data (partial sync)
- **QUEUED** — Record awaiting sync from ComicVine API queue

**Related Models:**

- All models in MODELS inherit from [`ComicvineSyncModel`](../../utils/models.md#comicvinesyncmodel) with `comicvine_status` field

**See Also:**

- [`ApiQueueCollector`](api_queue.md) — API queue counts
- [`MongoCollector`](mongo.md) — MongoDB cache counts
- [`metrics_view()`](../views.md#metrics_view) — Combines all collectors for `/metrics/` endpoint