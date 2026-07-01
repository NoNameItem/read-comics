# Publishers Spider

MongoDB collection: `comicvine_publishers`

## Summary

Fetches comic book publisher data from ComicVine API. Publishers are organizations that produce comics (Marvel, DC, Image, etc.).

- **List phase**: Gets basic publisher information (7 fields: ID, name, image, aliases, deck, URLs)
- **Detail phase**: Gets complete publisher data (8 fields: adds full description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine publisher identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this publisher |
| `site_detail_url` | URL | ComicVine website URL for this publisher |
| `name` | String | Publisher company name |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary description of the publisher |
| `image` | Object | Image object containing multiple URL sizes (logo) |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description of the publisher |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439018"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/publisher/1-marvel/",
  "site_detail_url": "https://comicvine.gamespot.com/publisher/1-marvel/",
  "name": "Marvel",
  "aliases": "Marvel Comics|Timely Comics|Marvel Entertainment",
  "deck": "Comic book publisher founded in 1939",
  "description": "<p><strong>Marvel</strong> is one of the largest American comic book publishers. Founded in 1939 (originally as Timely Comics), Marvel has created and published many iconic characters including Spider-Man, the Avengers, the X-Men, and the Fantastic Four...</p>",
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/marvel_logo.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/1/marvel_logo.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/1/marvel_logo.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/1/marvel_logo.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/1/marvel_logo.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/1/marvel_logo.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/1/marvel_logo.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/1/marvel_logo.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/marvel_logo.jpg"
  },
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only publishers modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates by ID with description and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Publisher Model](../../publishers/models.md) — PostgreSQL database model definition (if exists)
- [Publishers API](../../publishers/api) — REST API structure (if exists)