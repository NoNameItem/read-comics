# ImageSpider

## Summary

- **`ImageSpider`** — Specialized spider for fetching image metadata only (all 11 entity types)

## Reference

### ImageSpider

Scrapy spider that fetches image URLs and metadata for all entity types from ComicVine API. Unlike other spiders, ImageSpider only retrieves image data (no description or detailed fields).

**Inheritance**: `scrapy.Spider`

**Spider name**: `image_spider`

#### Configuration

**RESOURCES** (dict):
Maps resource names to MongoDB collections:
```python
{
    "characters": "comicvine_characters",
    "concepts": "comicvine_concepts",
    "issues": "comicvine_issues",
    "locations": "comicvine_locations",
    "objects": "comicvine_objects",
    "people": "comicvine_people",
    "publishers": "comicvine_publishers",
    "story_arcs": "comicvine_story_arcs",
    "teams": "comicvine_teams",
    "volumes": "comicvine_volumes",
}
```

**LIST_URL_PATTERN**:
```
https://comicvine.gamespot.com/api/{resource}/?format=json&field_list=id,name,api_detail_url,image&sort=id:asc&offset={offset}&limit={limit}&api_key={api_key}
```

**LIMIT**: 100 results per page (larger than regular spiders)

**Fields fetched**:
- `id` — ComicVine ID
- `name` — Entity name
- `api_detail_url` — ComicVine API URL
- `image` — Image object with URLs

#### Constructor Parameters

```python
def __init__(self, api_key=None, mongo_url=None, **kwargs):
    self.api_key = api_key        # Single API key (not list)
    self.mongo_url = mongo_url    # MongoDB connection URL
```

#### Key Methods

| Method | Purpose |
|--------|---------|
| `from_crawler(cls, crawler, *args, **kwargs)` | Initialize from Scrapy crawler; get settings |
| `start_requests()` | Yield requests for all 10 resources |
| `construct_list_url(resource, offset)` | Build ComicVine API URL for resource |
| `parse_list(response)` | Parse list JSON; yield paginated requests and items |
| `parse(response, **kwargs)` | Not implemented (required by Scrapy) |

#### Custom Request Classes

**ResourceRequest** (extends `scrapy.Request`):
- Adds `resource` attribute (resource name like "characters")
- Tracks which resource endpoint this request belongs to

#### MongoDB Output

Items are yielded with `_collection` wrapper:
```python
{
    "_collection": collection_name,  # MongoDB collection
    "item": {
        "id": 12345,
        "name": "Entity Name",
        "api_detail_url": "https://...",
        "crawl_date": "2024-01-15T...",
        "image": {
            "icon_url": "...",
            "medium_url": "...",
            "screen_url": "...",
            "small_url": "...",
            "super_url": "...",
            "thumb_url": "...",
            "tiny_url": "..."
        }
    }
}
```

#### Pagination

- Fetches all resources simultaneously (via parallel requests)
- Paginates through results for each resource independently
- Calculates next page based on:
  - `offset` (current page start)
  - `number_of_page_results` (items on current page)
  - `number_of_total_results` (total available)

**Formula**: `offset + number_of_page_results < number_of_total_results` → fetch next page

#### Use Cases

**When to use ImageSpider**:
- Quick image URL sync across all entities
- Updating thumbnail/image URLs without fetching full data
- Populating S3 bucket metadata
- Fast refresh of image information

**When NOT to use**:
- Need description or full details
- Only updating specific entities (not all 11 types)
- Incremental updates (no incremental support)

#### Differences from BaseSpider-based spiders

| Feature | ImageSpider | EntitySpider |
|---------|------------|-------------|
| **Endpoints** | All 10 resources | Single entity type |
| **Fields** | image only | List + Detail fields |
| **Incremental** | Not supported | Supported |
| **Skip existing** | Not implemented | Supported via middleware |
| **Detail fetching** | No | Yes (2-phase crawl) |
| **Per-page limit** | 100 | 50 |