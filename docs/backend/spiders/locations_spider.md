# Locations Spider

MongoDB collection: `comicvine_locations`

## Summary

Fetches comic book location/setting data from ComicVine API. Locations represent places in the comic universe (cities, buildings, planets, dimensions).

- **List phase**: Gets basic location information (9 fields: ID, name, image, first appearance, aliases, start year)
- **Detail phase**: Gets complete location data (10 fields: adds full description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine location identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this location |
| `site_detail_url` | URL | ComicVine website URL for this location |
| `name` | String | Location name |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary description of the location |
| `image` | Object | Image object containing multiple URL sizes |
| `first_appeared_in_issue` | Reference | Issue object where location first appeared |
| `start_year` | Integer | Year location was first introduced in comics |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description of the location |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439014"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/location/1-new-york-city/",
  "site_detail_url": "https://comicvine.gamespot.com/location/1-new-york-city/",
  "name": "New York City",
  "aliases": "NYC|Manhattan|New York",
  "deck": "Major city and home to many Marvel superheroes",
  "description": "<p><strong>New York City</strong> is one of the most frequently featured locations in comics, serving as home base for many superheroes including Spider-Man, the Avengers, and the Fantastic Four...</p>",
  "start_year": 1961,
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/location_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/1/location_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/1/location_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/1/location_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/1/location_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/1/location_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/1/location_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/1/location_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/location_image.jpg"
  },
  "first_appeared_in_issue": {
    "api_detail_url": "https://comicvine.gamespot.com/api/issue/100/",
    "id": 100,
    "name": "Spider-Man #1",
    "site_detail_url": "https://comicvine.gamespot.com/issue/100/"
  },
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only locations modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates by ID with description and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Location Model](../../locations/models.md) — PostgreSQL database model definition
- [Locations API](../../locations/api) — REST API structure