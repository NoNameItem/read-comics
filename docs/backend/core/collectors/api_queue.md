# API Queue Collector

Prometheus metrics collector for ComicVine API queue statistics.

## Summary

- [`ApiQueueCollector`](#apiqueuecollector) — Collects metrics on items waiting in API sync queue

## Reference

### `ApiQueueCollector`

Collects count of items in ComicVine API queue, grouped by endpoint.

**Base Class:** [`BaseCollector`](base.md#basecollector)

**Metrics Registered:**

- `read_comics_api_queue_count` (Gauge, "Number of items in comicvine API queue")
  - Labels: `endpoint` (string, e.g., "characters", "issues")
  - Values: Count of APIQueue records for that endpoint

**Behavior:**

- Queries `APIQueue` model grouping by endpoint
- Uses Django ORM `Count` aggregation for efficient counting
- Sets metric value for each endpoint with pending sync items
- Metric is a Gauge (can increase/decrease as items are queued/processed)

**Implementation:**

```python
def collect(self):
    # Query database for queue counts by endpoint
    queues = APIQueue.objects.values("endpoint").annotate(count=Count("comicvine_id"))

    # Register metric
    self._register_metric("read_comics_api_queue_count", help_string="...")

    # Set value for each endpoint
    for queue in queues:
        self._set_metric("read_comics_api_queue_count",
                        {"endpoint": queue["endpoint"]},
                        queue["count"])
```

**Example Output (Prometheus format):**

```
# HELP read_comics_api_queue_count Number of items in comicvine API queue
# TYPE read_comics_api_queue_count gauge
read_comics_api_queue_count{endpoint="characters"} 42
read_comics_api_queue_count{endpoint="issues"} 156
read_comics_api_queue_count{endpoint="teams"} 8
```

**Related Models:**

- [`APIQueue`](../../missing_issues/models.md) — Queue of pending ComicVine API sync items

**See Also:**

- [`DBCollector`](db.md) — Database row counts
- [`MongoCollector`](mongo.md) — MongoDB document counts
- [`metrics_view()`](../views.md#metrics_view) — Combines all collectors for `/metrics/` endpoint