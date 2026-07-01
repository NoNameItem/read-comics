# Spiders Infrastructure

Shared utilities and configuration for Scrapy spider execution and MongoDB integration.

## Summary

- **`mongo_connection.py`** — MongoDB connection management
- **`middlewares.py`** — Scrapy middlewares for rate limiting and skip logic
- **`pipelines.py`** — MongoPipeline for storing scraped data
- **`settings.py`** — Scrapy configuration
- **`scrappyscript/__init__.py`** — Job/Processor for running spiders from Python/Celery

## Reference

### mongo_connection.py

**Class**: `Connect`

Simple MongoDB connection wrapper:

```python
@staticmethod
def get_connection(url):
    return MongoClient(url)
```

**Usage**: `mongo_client = Connect.get_connection(settings.MONGO_URL)`

---

### middlewares.py

#### TooManyRequestsRetryMiddleware

Custom retry middleware for ComicVine API 429/420 rate limit responses.

**Configuration**:
- `DEFAULT_DELAY` = 600 seconds (if no Retry-After header)
- `MAX_DELAY` = 7200 seconds (cap on Retry-After values)

**Behavior**:
1. Detects 429/420 status codes
2. Reads `Retry-After` header if present
3. Waits up to MAX_DELAY seconds before retrying
4. Pauses/unpauses Twisted reactor during wait

**Method**: `async process_response(request, response, spider)`

---

#### SkipExistingRequestsMiddleware

Middleware for `skip_existing="Y"` mode. Skips detail page requests if entity already cached with `crawl_source: "detail"`.

**Configuration**:
- Checks `spider.skip_existing` attribute
- Reads `check_comicvine_id` from request meta

**Behavior**:
1. Queries MongoDB for existing `crawl_source: "detail"` documents
2. Raises `IgnoreRequest` if found (skips request)
3. Logs skipped requests

**Method**: `process_request(request, spider)`

---

### pipelines.py

#### MongoPipeline

Scrapy item pipeline that stores items in MongoDB.

**Configuration**:
- Reads `MONGO_URL` from Scrapy settings
- Uses spider name as collection name (unless `_collection` in item)

**Input**:
```python
item = {
    "id": 12345,
    "name": "Entity Name",
    "crawl_date": "2024-01-15T...",
    "crawl_source": "detail"
    # ... other fields
}
```

**Behavior**:
1. Gets MongoDB connection
2. Determines collection name:
   - From `item["_collection"]` if present
   - Otherwise from `spider.name`
3. Extracts item if `_collection` wrapper present
4. Skips saving if `item["skip"] == True`
5. Upserts item: `db[collection].update_one({"id": item["id"]}, {"$set": dict(item)}, upsert=True)`
6. Returns stub: `{"id": item["id"]}`

**Output**:
```json
{"id": 12345}
```

---

### settings.py

Scrapy configuration file.

**Key Settings**:

| Setting | Value | Purpose |
|---------|-------|---------|
| `BOT_NAME` | `"comicvine_crawler"` | Bot identifier |
| `LOG_LEVEL` | `"INFO"` | Logging level |
| `SPIDER_MODULES` | `["read_comics.spiders.spiders"]` | Spider discovery path |
| `USER_AGENT` | `"comicvine_crawler read-comics.net"` | HTTP User-Agent header |
| `ROBOTSTXT_OBEY` | `False` | Don't block based on robots.txt |
| `CONCURRENT_REQUESTS` | `1` | Sequential requests only |
| `DOWNLOAD_DELAY` | `3` seconds (default) | Delay between requests |
| `CONCURRENT_REQUESTS_PER_DOMAIN` | `1` | One request per domain at a time |

**Environment Variables**:
- `SCRAPPY_DOWNLOAD_DELAY` — Override default download delay (default: 3)

---

### scrappyscript/__init__.py

Python runner for executing Scrapy spiders from Django/Celery context.

#### Job

Wrapper for a single spider execution request.

```python
class Job:
    def __init__(self, spider, *args, **kwargs):
        self.spider = spider        # Spider class (not instance)
        self.args = args            # Positional args for spider __init__
        self.kwargs = kwargs        # Keyword args for spider __init__
```

**Usage**:
```python
job = Job(CharactersSpider, incremental="Y", skip_existing="N")
```

---

#### Processor

Process manager that runs Scrapy crawler in isolated subprocess.

**Inheritance**: `billiard.Process` (Celery-compatible fork of multiprocessing.Process)

**Constructor**:
```python
def __init__(self, settings=None, ignore_results=True):
    self.settings = settings or Settings()  # Scrapy Settings
    self.items = []                          # Accumulated items
    self.ignore_results = ignore_results     # Discard or return items
```

**Methods**:

| Method | Purpose |
|--------|---------|
| `run(jobs)` | Execute one or more Job objects in subprocess; return accumulated items |
| `validate(jobs)` | Check all jobs are Job instances |
| `_crawl(requests)` | Internal: Start CrawlerProcess and run jobs |

**Usage**:
```python
processor = Processor(settings=spider_settings)
job = Job(CharactersSpider, incremental="Y")
results = processor.run(job)  # Returns list of items scraped
```

**Key Features**:
- Runs in separate process (billiard subprocess)
- Signals connected to item_scraped signal (if `ignore_results=False`)
- Returns results via inter-process queue
- Terminates subprocess cleanly after completion

**Exceptions**:
- `ScrapyScriptException` — Raised if jobs list contains non-Job objects
