# API viewsets

## `BaseStatsViewSet`

- Simplifies collection-level statistics for `ComicvineSyncModel` subclasses.
- Exposes the following `GET` actions (all routed via `@action(detail=False)`):
  - `/mongo_count/`: total documents in the Mongo collection configured by `mongo_collection`.
  - `/mongo_list_count/`: documents where `crawl_source=list`.
  - `/mongo_detail_count/`: documents where `crawl_source=detail`.
  - `/db_count/`: total rows in the relational model.
  - `/matched_count/`, `/not_matched_count/`, `/queued_count/`: convenience counters wrapped in JSON responses.
- Designed for internal dashboards and Celery/maintenance tooling that needs quick import statistics.
