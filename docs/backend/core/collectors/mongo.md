# MongoDB Collector

Prometheus metrics collector for MongoDB cache statistics.

## Summary

- [`MongoCollector`](#mongocollector) — Collects metrics on MongoDB documents cached from ComicVine API

## Reference

### `MongoCollector`

Collects database metrics on document counts in MongoDB collections, broken down by crawl source (API list vs detail pages).

**Base Class:** [`BaseCollector`](base.md#basecollector)

**MongoDB Collections Tracked:**

```python
COLLECTIONS = {
    "characters": "comicvine_characters",
    "concepts": "comicvine_concepts",
    "issues": "comicvine_issues",
    "locations": "comicvine_locations",
    "objects": "comicvine_objects",
    "people": "comicvine_people",
    "powers": "comicvine_powers",
    "publishers": "comicvine_publishers",
    "story_arcs": "comicvine_story_arcs",
    "teams": "comicvine_teams",
    "volumes": "comicvine_volumes",
}
```

**Metrics Registered:**

- `read_comics_mongo_count` (Gauge, "Number of documents in mongo collection")
  - Labels:
    - `collection` (string): Collection name or "total"
    - `source` (string): Data source type
  - Sources:
    - `"all"` — Total documents in collection
    - `"list"` — Documents from ComicVine list API pages
    - `"detail"` — Documents from ComicVine detail pages

**Behavior:**

- Connects to MongoDB using `settings.MONGO_URL`
- For each collection:
  - Aggregates documents grouping by `crawl_source` field
  - Sets metric values for each source breakdown
  - Increments running totals under `collection="total"`
- Closes MongoDB connection after collecting metrics
- Uses MongoDB `$group` aggregation for efficient counting

**Implementation:**

```python
def collect(self):
    # Connect to MongoDB
    self.client = MongoClient(settings.MONGO_URL)
    self.db = self.client.get_default_database()

    # Register metric
    self._register_metric("read_comics_mongo_count", help_string="...")

    # Query each collection
    for k, v in self.COLLECTIONS.items():
        counts_query = self.db[v].aggregate([
            {"$group": {"_id": "$crawl_source", "count": {"$sum": 1}}}
        ])
        # Set metric values for each source...

    # Close connection
    self.client.close()
```

**Example Output (Prometheus format):**

```
# HELP read_comics_mongo_count Number of documents in mongo collection
# TYPE read_comics_mongo_count gauge
read_comics_mongo_count{collection="characters",source="all"} 5000
read_comics_mongo_count{collection="characters",source="list"} 3200
read_comics_mongo_count{collection="characters",source="detail"} 1800
read_comics_mongo_count{collection="issues",source="all"} 500000
read_comics_mongo_count{collection="issues",source="list"} 350000
read_comics_mongo_count{collection="issues",source="detail"} 150000
...
read_comics_mongo_count{collection="total",source="all"} 2000000
read_comics_mongo_count{collection="total",source="list"} 1400000
read_comics_mongo_count{collection="total",source="detail"} 600000
```

**Data Source Meanings:**

- **"list"** — Document fetched from ComicVine list API endpoint (mass data)
- **"detail"** — Document fetched from ComicVine detail endpoint (detailed info)
- **"all"** — Combined total of both sources

**MongoDB Configuration:**

- Connection: `settings.MONGO_URL` (e.g., `mongodb://localhost:27017/comicvine_cache`)
- Database: Default database from connection string
- Field mapping: Documents must contain `crawl_source` field with value "list" or "detail"

**Related:**

- Scrapy pipelines populate MongoDB via `crawl_source` field
- Data flows from MongoDB → PostgreSQL via Celery tasks
- Connection closed after metrics collection to avoid hanging connections

**See Also:**

- [`DBCollector`](db.md) — PostgreSQL record counts
- [`ApiQueueCollector`](api_queue.md) — API queue counts
- [`metrics_view()`](../views.md#metrics_view) — Combines all collectors for `/metrics/` endpoint