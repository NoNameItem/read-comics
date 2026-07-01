# FullSpider

## Summary

- **`FullSpider`** — Unified spider for fetching all 11 entity types in single spider run

## Reference

### FullSpider

Scrapy spider that crawls all entity endpoints (Character, Concept, Issue, Location, Object, People, Power, Publisher, StoryArc, Team, Volume) in parallel within single spider process.

**Inheritance**: `scrapy.Spider`

**Spider name**: `full_spider`

#### Configuration

**ENDPOINTS** (11 total):
- Endpoint(collection, endpoint_name, list_fields, detail_fields)
- All defined as class-level tuple

**LIST_URL_PATTERN**:
```
https://comicvine.gamespot.com/api/{endpoint}/?format=json&field_list={list_url_fields}&sort=id:asc&offset={offset}&limit={limit}&api_key={api_key}
```

**LIMIT**: 50 results per page

#### Constructor Parameters

Same as `BaseSpider`:
```python
def __init__(
    self,
    incremental="Y",      # Only fetch updated entities
    api_keys=None,        # List of ComicVine API keys
    filters=None,         # Dict of ComicVine filters
    skip_existing="N",    # Skip entities with existing detail data
    mongo_url=None,       # MongoDB connection URL
    **kwargs
)
```

#### Key Methods

| Method | Purpose |
|--------|---------|
| `from_crawler(cls, crawler, *args, **kwargs)` | Initialize from Scrapy crawler; setup incremental filters |
| `start_requests()` | Yield first page request for each of 11 endpoints |
| `construct_list_url(endpoint, list_url_fields, offset)` | Build ComicVine list URL |
| `construct_detail_url(url, field_list=None)` | Append API key and field_list to detail URL |
| `parse_list(response)` | Parse list JSON; yield items and detail requests |
| `parse_detail(response)` | Parse detail JSON and return enriched item |

#### Custom Request Classes

**EndpointRequest** (extends `scrapy.Request`):
- Adds `endpoint` attribute (Endpoint dataclass)
- Tracks which endpoint this request belongs to

**Endpoint** (dataclass):
```python
@dataclass
class Endpoint:
    collection: str         # MongoDB collection name
    endpoint: str          # API endpoint (e.g., "characters")
    list_url_fields: str   # Comma-separated field list for list requests
    detail_url_fields: str # Comma-separated field list for detail requests
```

#### MongoDB Output

Items are yielded with `_collection` wrapper:
```python
{
    "_collection": endpoint.collection,  # MongoDB collection name
    "item": {
        "id": 12345,
        "name": "...",
        "crawl_source": "list",
        "crawl_date": "2024-01-15T..."
    }
}
```

MongoPipeline extracts `item` and stores in specified collection.

#### Comparison to Individual Spiders

| Aspect | FullSpider | Individual Spiders |
|--------|-----------|-------------------|
| **Endpoints** | All 11 in one spider | One endpoint per spider |
| **MongoDB collections** | 11 collections populated | 1 collection populated |
| **Run time** | Parallel requests across endpoints | Sequential spider runs |
| **Use case** | Full sync in one job | Incremental updates per entity |

#### Usage

```python
from read_comics.spiders.scrappyscript import Job, Processor

processor = Processor(settings=spider_settings)
job = Job(FullSpider, incremental="Y", skip_existing="N")
processor.run(job)
```

**Advantages**:
- Single spider process instead of 11
- Shared session/connection management
- Simultaneous requests across multiple endpoints
- Efficient for full syncs

**Disadvantages**:
- Complex Endpoint configuration
- All-or-nothing execution (can't skip specific endpoints)
- Harder to debug individual entity crawls