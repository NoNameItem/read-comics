# Base Spider

## Summary

- **`BaseSpider`** — Scrapy base spider for ComicVine API crawling with pagination, incremental sync, and skip-existing logic
- **`SpiderImplementationError`** — Exception for incomplete spider subclass implementations

## Reference

### BaseSpider

Base class for all entity-specific spiders. Handles ComicVine API pagination, incremental updates, and MongoDB caching.

**Inheritance**: `scrapy.Spider`

#### Class Attributes

| Attribute | Type | Purpose |
|-----------|------|---------|
| `LIST_URL_PATTERN` | str | ComicVine API list endpoint URL template with placeholders for `{limit}`, `{offset}`, `{api_key}` |
| `DETAIL_FIELD_LIST` | str | Comma-separated ComicVine field list for detail endpoint requests |
| `LIMIT` | int | Results per page (default 50) |
| `name` | str | Spider identifier (e.g., `comicvine_characters`) - must match MongoDB collection name |

#### Constructor Parameters

```python
def __init__(
    self,
    incremental="N",        # "Y" = only fetch updated entities since last run
    api_keys=None,          # List of ComicVine API keys
    filters=None,           # Dict of ComicVine filters (e.g., {"date_last_updated": "range"})
    skip_existing="N",      # "Y" = skip entities already cached in detail form
    mongo_url=None,         # MongoDB connection URL
    **kwargs
)
```

**Parameters**:
- `incremental` — If `"Y"`, queries MongoDB `spider_info` for last run timestamp and only fetches recently updated entities
- `skip_existing` — If `"Y"`, middleware skips fetching detail pages for entities already cached with `crawl_source="detail"`
- `filters` — Dictionary of ComicVine API filters appended to list URL
- `api_keys` — List of API keys (random selected per request for load distribution)
- `mongo_url` — MongoDB connection string

#### Key Methods

| Method | Purpose |
|--------|---------|
| `from_crawler(cls, crawler, *args, **kwargs)` | Initializes spider from Scrapy crawler context; sets up incremental filter if needed |
| `start_requests()` | Yields first page list URL request |
| `construct_list_url(offset)` | Builds ComicVine list endpoint URL with filters and pagination |
| `construct_detail_url(url)` | Appends API key and field_list to detail endpoint URL |
| `parse_list(response)` | Parses list JSON; yields list-level items and detail page requests |
| `parse_detail(response)` | Parses detail JSON and returns enriched item |
| `parse(response)` | Not implemented (required by Scrapy but unused) |

#### Incremental Update Logic

When `incremental="Y"`:
1. Queries MongoDB `spider_info` collection for last run timestamp
2. Calculates `date_last_updated` filter (previous run time - 1 hour)
3. Adds filter to API URL to fetch only recently updated entities
4. Updates `spider_info` with current run timestamp after spider finishes

#### Skip Existing Logic

When `skip_existing="Y"` (via middleware):
1. Checks MongoDB for entities with `crawl_source="detail"`
2. Skips fetching detail page if entity already has detail-level data
3. Logs skipped entities
4. Returns stub item with `skip: True`

#### Response Processing

**List endpoint (`parse_list`):**
1. Parses JSON response
2. Checks total results to calculate pagination
3. Yields list-level items with `crawl_source="list"`
4. Yields requests for detail endpoints (priority 1)
5. Yields requests for next list page (priority 5)
6. Filters by `skip_existing` status

**Detail endpoint (`parse_detail`):**
1. Parses JSON detail response
2. Adds metadata: `crawl_date`, `crawl_source="detail"`
3. Returns complete item

#### Crawl Source Tracking

MongoDB stores two versions of each entity:

| crawl_source | When | Fields |
|--------------|------|--------|
| `list` | First pass | Basic fields from list endpoint |
| `detail` | Full fetch | Complete fields from detail endpoint |

Detail version overwrites list version (via upsert). Skip-existing logic prevents re-fetching detail if present.

#### Exceptions

- **`SpiderImplementationError`** — Raised if subclass doesn't define `LIST_URL_PATTERN`