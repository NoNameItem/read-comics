# People Spider

MongoDB collection: `comicvine_people`

## Summary

Fetches comic book creator/person data from ComicVine API. People are real-world individuals who created comics (writers, artists, editors, etc.) or individuals within comic universes.

- **List phase**: Gets basic person information (11 fields: ID, name, image, birth, country, death, hometown, aliases, deck)
- **Detail phase**: Gets complete person data (12 fields: adds full biography/description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine person identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this person |
| `site_detail_url` | URL | ComicVine website URL for this person |
| `name` | String | Person's name |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary (profession, role, or description) |
| `image` | Object | Image object containing multiple URL sizes |
| `birth` | String | Birth date in YYYY-MM-DD format |
| `country` | String | Country of origin |
| `death` | String | Death date in YYYY-MM-DD format (if deceased) |
| `hometown` | String | Hometown/birthplace |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted biography |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439016"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/person/1-stan-lee/",
  "site_detail_url": "https://comicvine.gamespot.com/person/1-stan-lee/",
  "name": "Stan Lee",
  "aliases": "Stanley Martin Lieber|Stan the Man",
  "deck": "Comic book writer and former publisher of Marvel Comics",
  "description": "<p><strong>Stan Lee</strong> is one of the most famous comic book creators and the former publisher of Marvel Comics. He co-created the Fantastic Four, the Hulk, Spider-Man, X-Men, and many other iconic characters...</p>",
  "birth": "1922-12-28",
  "death": "2018-11-12",
  "country": "United States",
  "hometown": "New York City",
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/person_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/1/person_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/1/person_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/1/person_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/1/person_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/1/person_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/1/person_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/1/person_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/person_image.jpg"
  },
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only people modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates by ID with biography and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Person Model](../../people/models.md) — PostgreSQL database model definition
- [People API](../../people/api) — REST API structure