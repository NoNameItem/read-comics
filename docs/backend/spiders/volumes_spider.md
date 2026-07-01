# Volumes Spider

MongoDB collection: `comicvine_volumes`

## Summary

Fetches comic book volume/series data from ComicVine API. Volumes represent ongoing comic book series (e.g., "The Amazing Spider-Man", "Uncanny X-Men").

- **List phase**: Gets basic volume information (10 fields: ID, name, image, first/last issues, publisher, start year, aliases, deck)
- **Detail phase**: Gets complete volume data (11 fields: adds full description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine volume identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this volume |
| `site_detail_url` | URL | ComicVine website URL for this volume |
| `name` | String | Volume/series name |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary description of the volume |
| `image` | Object | Image object containing multiple URL sizes |
| `first_issue` | Reference | Issue object of the first issue in this volume |
| `last_issue` | Reference | Issue object of the most recent or final issue |
| `publisher` | Reference | Publisher object that publishes/published this volume |
| `start_year` | Integer | Year the volume was first published |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description of the volume |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd79943901b"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/volume/1-the-amazing-spider-man/",
  "site_detail_url": "https://comicvine.gamespot.com/volume/1-the-amazing-spider-man/",
  "name": "The Amazing Spider-Man",
  "aliases": "Amazing Spider-Man|Spider-Man|ASM",
  "deck": "The primary ongoing series featuring Spider-Man",
  "description": "<p><strong>The Amazing Spider-Man</strong> is Marvel's flagship Spider-Man series, running continuously since 1963 (with some gaps). The series features the adventures of Peter Parker/Spider-Man as he balances his life as a superhero with personal relationships...</p>",
  "start_year": 1963,
  "publisher": {
    "api_detail_url": "https://comicvine.gamespot.com/api/publisher/1/",
    "id": 1,
    "name": "Marvel",
    "site_detail_url": "https://comicvine.gamespot.com/publisher/1/"
  },
  "first_issue": {
    "api_detail_url": "https://comicvine.gamespot.com/api/issue/1000/",
    "id": 1000,
    "name": "The Amazing Spider-Man #1",
    "site_detail_url": "https://comicvine.gamespot.com/issue/1000/"
  },
  "last_issue": {
    "api_detail_url": "https://comicvine.gamespot.com/api/issue/2000/",
    "id": 2000,
    "name": "The Amazing Spider-Man #999",
    "site_detail_url": "https://comicvine.gamespot.com/issue/2000/"
  },
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/volume_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/1/volume_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/1/volume_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/1/volume_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/1/volume_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/1/volume_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/1/volume_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/1/volume_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/volume_image.jpg"
  },
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only volumes modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates by ID with description and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field
- **Key references**: Contains references to first and last issues in the series, allowing traversal of the volume's issue list

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Volume Model](../../volumes/models.md) — PostgreSQL database model definition
- [Volumes API](../../volumes/api) — REST API structure