# Collectors

Prometheus metrics collectors for monitoring system status.

## Documentation

- [**base.md**](base.md) — `MetricValue`, `Metric`, `BaseCollector`, and `labels_to_string()` utility
- [**api_queue.md**](api_queue.md) — `ApiQueueCollector` for API sync queue metrics
- [**db.md**](db.md) — `DBCollector` for PostgreSQL record counts
- [**mongo.md**](mongo.md) — `MongoCollector` for MongoDB cache statistics

## Overview

Collectors are responsible for gathering metrics from different data sources and formatting them in Prometheus text format for the `/metrics/` endpoint.

- `BaseCollector` — Abstract base with metric registration, storage, and reporting
- Subclasses implement `collect()` to gather data from their respective sources
- All metrics use label-based organization (Prometheus format)

See [`metrics_view()`](../views.md#metrics_view) for how collectors are used together.