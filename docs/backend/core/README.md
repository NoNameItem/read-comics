# Core

System monitoring and metrics collection for Prometheus.

## Documentation

### Main Views

- [**views.md**](views.md) — `metrics_view()` endpoint for Prometheus metrics (includes HomeView, NewIssuesView)

### Collectors

Prometheus metrics collectors in `collectors/` subdirectory:

- [**collectors/base.md**](collectors/base.md) — Base classes: `MetricValue`, `Metric`, `BaseCollector`, `labels_to_string()` utility
- [**collectors/api_queue.md**](collectors/api_queue.md) — API sync queue metrics
- [**collectors/db.md**](collectors/db.md) — PostgreSQL record counts by model and sync status
- [**collectors/mongo.md**](collectors/mongo.md) — MongoDB cache document counts

## Key Modules

- `views.py` — HTTP views: `metrics_view()` for `/metrics/` endpoint, `HomeView`, `NewIssuesView`
- `collectors/base.py` — Base classes and utilities for metrics: `MetricValue`, `Metric`, `BaseCollector`
- `collectors/api_queue.py` — `ApiQueueCollector` for API sync queue metrics
- `collectors/db.py` — `DBCollector` for PostgreSQL statistics
- `collectors/mongo.py` — `MongoCollector` for MongoDB cache statistics

## Monitoring Endpoint

The `/metrics/` endpoint aggregates metrics from all collectors for Prometheus scraping:

```
GET /metrics/  →  Prometheus text format
```

Metrics included:
- **MongoDB cache**: documents per entity type, by data source (list/detail)
- **PostgreSQL**: records per model, by sync status (matched/not_matched/queued)
- **API queue**: pending items per endpoint waiting for ComicVine sync
