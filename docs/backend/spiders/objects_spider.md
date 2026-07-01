# Objects Spider

MongoDB collection: `comicvine_objects`

## Summary

Fetches comic book object/technology data from ComicVine API. Objects represent items, gadgets, weapons, and technology in comics (e.g., "Iron Man Suit", "Batmobile", "Infinity Gems").

- **List phase**: Gets basic object information (9 fields: ID, name, image, first appearance, aliases, start year)
- **Detail phase**: Gets complete object data (10 fields: adds full description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine object identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this object |
| `site_detail_url` | URL | ComicVine website URL for this object |
| `name` | String | Object/item name |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary description of the object |
| `image` | Object | Image object containing multiple URL sizes |
| `first_appeared_in_issue` | Reference | Issue object where object first appeared |
| `start_year` | Integer | Year object was first introduced in comics |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description of the object |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439015"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/object/1-iron-man-suit/",
  "site_detail_url": "https://comicvine.gamespot.com/object/1-iron-man-suit/",
  "name": "Iron Man Suit",
  "aliases": "Mark I|Iron Armor|Power Armor",
  "deck": "Tony Stark's powered armor suit",
  "description": "<p>The <strong>Iron Man Suit</strong> is Tony Stark's greatest invention - a powered exoskeleton that grants superhuman strength, flight, and advanced weaponry...</p>",
  "start_year": 1963,
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/object_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/1/object_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/1/object_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/1/object_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/1/object_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/1/object_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/1/object_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/1/object_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/object_image.jpg"
  },
  "first_appeared_in_issue": {
    "api_detail_url": "https://comicvine.gamespot.com/api/issue/200/",
    "id": 200,
    "name": "Tales of Suspense #39",
    "site_detail_url": "https://comicvine.gamespot.com/issue/200/"
  },
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only objects modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates by ID with description and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Object Model](../../objects/models.md) — PostgreSQL database model definition
- [Objects API](../../objects/api) — REST API structure