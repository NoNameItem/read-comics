# Powers Spider

MongoDB collection: `comicvine_powers`

## Summary

Fetches comic book power/ability data from ComicVine API. Powers represent superhuman abilities, superpowers, and special skills (e.g., "Flight", "Telepathy", "Super Strength").

- **List phase**: Gets basic power information (4 fields: ID, name, aliases, URLs)
- **Detail phase**: Gets complete power data (5 fields: adds full description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine power identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this power |
| `site_detail_url` | URL | ComicVine website URL for this power |
| `name` | String | Power/ability name |
| `aliases` | String | Pipe-separated list of alternative names |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description of the power |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439017"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/power/1-flight/",
  "site_detail_url": "https://comicvine.gamespot.com/power/1-flight/",
  "name": "Flight",
  "aliases": "Flying|Levitation|Aerial locomotion",
  "description": "<p><strong>Flight</strong> is the ability to propel oneself through the air and achieve sustained aerial locomotion. This power is one of the most common superpowers in comics, possessed by characters like Superman, Wonder Woman, and many others...</p>",
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only powers modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates by ID with description and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Power Model](../../powers/models.md) — PostgreSQL database model definition
- [Powers API](../../powers/api) — REST API structure (if available)