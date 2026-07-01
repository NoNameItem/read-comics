# Concepts Spider

MongoDB collection: `comicvine_concepts`

## Summary

Fetches comic book concept/technology data from ComicVine API. Concepts represent themes, objects, ideas, and technologies used in comics (e.g., "Time Travel", "Cloning", "Artificial Intelligence").

- **List phase**: Gets basic concept information (9 fields: ID, name, image, first appearance, aliases)
- **Detail phase**: Gets complete concept data (10 fields: adds full description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine concept identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this concept |
| `site_detail_url` | URL | ComicVine website URL for this concept |
| `name` | String | Concept name |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary description of the concept |
| `image` | Object | Image object containing multiple URL sizes |
| `first_appeared_in_issue` | Reference | Issue object where concept first appeared |
| `start_year` | Integer | Year concept was first introduced in comics |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description of the concept |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "id": 10,
  "api_detail_url": "https://comicvine.gamespot.com/api/concept/10-time-travel/",
  "site_detail_url": "https://comicvine.gamespot.com/concept/10-time-travel/",
  "name": "Time Travel",
  "aliases": "Temporal displacement|Time machine|Time manipulation",
  "deck": "The ability or technology to move through time",
  "description": "<p><strong>Time Travel</strong> is a common concept in science fiction and comics where characters can move through different time periods...</p>",
  "start_year": 1961,
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/10/10_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/10/10_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/10/10_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/10/10_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/10/10_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/10/10_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/10/10_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/10/10_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/10/10_image.jpg"
  },
  "first_appeared_in_issue": {
    "api_detail_url": "https://comicvine.gamespot.com/api/issue/1000/",
    "id": 1000,
    "name": "The Flash #1",
    "site_detail_url": "https://comicvine.gamespot.com/issue/1000/"
  },
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only concepts modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document already has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates document by ID and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Concept Model](../../concepts/models.md) — PostgreSQL database model definition
- [Concepts API](../../concepts/api) — REST API structure