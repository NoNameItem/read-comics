# Teams Spider

MongoDB collection: `comicvine_teams`

## Summary

Fetches comic book team data from ComicVine API. Teams represent groups of superheroes that work together (e.g., "Avengers", "X-Men", "Fantastic Four").

- **List phase**: Gets basic team information (9 fields: ID, name, image, first appearance, aliases, publisher, deck)
- **Detail phase**: Gets complete team data (10 fields: adds full description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine team identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this team |
| `site_detail_url` | URL | ComicVine website URL for this team |
| `name` | String | Team name |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary description of the team |
| `image` | Object | Image object containing multiple URL sizes |
| `first_appeared_in_issue` | Reference | Issue object where team first appeared |
| `publisher` | Reference | Publisher object associated with this team |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description of the team |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd79943901a"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/team/1-avengers/",
  "site_detail_url": "https://comicvine.gamespot.com/team/1-avengers/",
  "name": "Avengers",
  "aliases": "The Avengers|Avengers Initiative",
  "deck": "Premier superhero team of the Marvel Universe",
  "description": "<p>The <strong>Avengers</strong> are Earth's Mightiest Heroes - a team of superheroes who have defended the world from countless threats. Founded by Iron Man, Thor, and the Hulk, the team has grown to include Captain America, Black Widow, Hawkeye, and many others...</p>",
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/avengers_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/1/avengers_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/1/avengers_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/1/avengers_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/1/avengers_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/1/avengers_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/1/avengers_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/1/avengers_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/avengers_image.jpg"
  },
  "first_appeared_in_issue": {
    "api_detail_url": "https://comicvine.gamespot.com/api/issue/300/",
    "id": 300,
    "name": "The Avengers #1",
    "site_detail_url": "https://comicvine.gamespot.com/issue/300/"
  },
  "publisher": {
    "api_detail_url": "https://comicvine.gamespot.com/api/publisher/1/",
    "id": 1,
    "name": "Marvel",
    "site_detail_url": "https://comicvine.gamespot.com/publisher/1/"
  },
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only teams modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates by ID with description and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Team Model](../../teams/models.md) — PostgreSQL database model definition
- [Teams API](../../teams/api) — REST API structure