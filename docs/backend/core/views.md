# Core Views

## Summary

- [`metrics_view()`](#metrics_view) — Aggregates all Prometheus metrics for monitoring endpoint

## Reference

### `metrics_view()`

HTTP view endpoint that collects and returns Prometheus-format metrics from all collectors.

**Signature:**

```python
def metrics_view(request) -> HttpResponse
```

**Parameters:**

- `request` (HttpRequest): Django HTTP request (unused, required by view interface)

**Returns:**

- `HttpResponse` with status 200
  - Content-Type: `text/plain`
  - Body: Prometheus metrics in text format

**Behavior:**

1. **Instantiates collectors:**
   - [`MongoCollector`](collectors/mongo.md#mongocollector) — MongoDB document counts
   - [`DBCollector`](collectors/db.md#dbcollector) — PostgreSQL record counts by sync status
   - [`ApiQueueCollector`](collectors/api_queue.md#apiqueuecollector) — API sync queue counts

2. **Collects metrics:**
   - Calls `.collect()` on each collector
   - Each collector gathers data and registers metrics

3. **Aggregates reports:**
   - Calls `.report()` on each collector
   - Concatenates all metrics in Prometheus text format
   - Mongo metrics + DB metrics + API queue metrics

4. **Returns response:**
   - Plain text response with all metrics
   - Suitable for Prometheus scraping

**Prometheus Output Format:**

```
# HELP <metric_name> <description>
# TYPE <metric_name> <type>
<metric_name>{<labels>} <value> <timestamp>
...
```

**Example Response:**

```
# HELP read_comics_mongo_count Number of documents in mongo collection
# TYPE read_comics_mongo_count gauge
read_comics_mongo_count{collection="characters",source="all"} 5000
read_comics_mongo_count{collection="characters",source="list"} 3200
...
# HELP read_comics_db_count Number of rows in database
# TYPE read_comics_db_count gauge
read_comics_db_count{status="all",table="characters"} 1250
read_comics_db_count{status="matched",table="characters"} 1200
...
# HELP read_comics_api_queue_count Number of items in comicvine API queue
# TYPE read_comics_api_queue_count gauge
read_comics_api_queue_count{endpoint="characters"} 42
read_comics_api_queue_count{endpoint="issues"} 156
...
```

**URL Configuration:**

Typically mounted at `/metrics/` endpoint for Prometheus scraping:

```python
# config/urls.py
urlpatterns = [
    path("metrics/", metrics_view, name="metrics"),
]
```

**Prometheus Configuration:**

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'read_comics'
    static_configs:
      - targets: ['localhost:8000/metrics/']
    scrape_interval: 15s
```

**Performance Notes:**

- MongoDB connection is established and closed per request
- Database queries use ORM aggregations (efficient)
- Suitable for monitoring endpoints with reasonable scrape intervals (15s+)
- No caching; metrics are freshly collected on each request

**Collectors Included:**

1. **MongoCollector** — Cache statistics
   - Documents per entity type
   - Breakdown by data source (list vs detail)

2. **DBCollector** — Production data statistics
   - Record counts per model
   - Breakdown by sync status (matched, not_matched, queued)
   - Total aggregates

3. **ApiQueueCollector** — Sync queue statistics
   - Pending items per endpoint
   - Useful for monitoring sync backlog

**See Also:**

- [`BaseCollector`](collectors/base.md#basecollector) — Base class for collectors
- [`MongoCollector`](collectors/mongo.md) — MongoDB metrics implementation
- [`DBCollector`](collectors/db.md) — PostgreSQL metrics implementation
- [`ApiQueueCollector`](collectors/api_queue.md) — API queue metrics implementation