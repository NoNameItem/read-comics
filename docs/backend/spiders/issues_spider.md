# Issues Spider

MongoDB collection: `comicvine_issues`

## Summary

Fetches comic book issue data from ComicVine API. Issues are the primary entity in the system - individual comic book publications.

- **List phase**: Gets basic issue information (10 fields: ID, name, issue number, cover date, volume, associated images)
- **Detail phase**: Gets comprehensive issue data (23 fields: adds full description, character/concept/story arc credits, credits for all entities)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine issue identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this issue |
| `site_detail_url` | URL | ComicVine website URL for this issue |
| `name` | String | Issue title/name |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary of the issue |
| `image` | Object | Cover image object containing multiple URL sizes |
| `issue_number` | String | Issue number (e.g., "1", "1.5", "Annual 1") |
| `cover_date` | String | Cover date in YYYY-MM-DD format |
| `store_date` | String | Store availability date in YYYY-MM-DD format |
| `volume` | Reference | Volume/series object this issue belongs to |
| `associated_images` | Array | Array of additional images associated with the issue |

### Detail Endpoint Fields (adds 13 fields to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description and plot summary |
| `character_credits` | Array | Array of character objects appearing in this issue |
| `character_died_in` | Array | Array of character objects that die in this issue |
| `concept_credits` | Array | Array of concept objects featured in this issue |
| `location_credits` | Array | Array of location objects featured in this issue |
| `object_credits` | Array | Array of object/technology objects in this issue |
| `person_credits` | Array | Array of people (creators: writers, artists, etc.) |
| `story_arc_credits` | Array | Array of story arc objects this issue is part of |
| `team_credits` | Array | Array of team objects appearing in this issue |
| `team_disbanded_in` | Array | Array of team objects disbanded in this issue |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439013"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/issue/1-amazing-fantasy-15/",
  "site_detail_url": "https://comicvine.gamespot.com/issue/1-amazing-fantasy-15/",
  "name": "With Great Power",
  "aliases": "Amazing Fantasy Vol 1 15",
  "deck": "The first appearance of Spider-Man",
  "description": "<p>This historic issue features the first appearance of Spider-Man, the amazing web-slinging hero...</p>",
  "issue_number": "15",
  "cover_date": "1962-06-01",
  "store_date": "1962-05-01",
  "volume": {
    "api_detail_url": "https://comicvine.gamespot.com/api/volume/1/",
    "id": 1,
    "name": "Amazing Fantasy",
    "site_detail_url": "https://comicvine.gamespot.com/volume/1/"
  },
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/1_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/1/1_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/1/1_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/1/1_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/1/1_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/1/1_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/1/1_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/1/1_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/1_image.jpg"
  },
  "associated_images": [
    {
      "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/alt_1.jpg",
      "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/alt_1.jpg"
    }
  ],
  "character_credits": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/character/1/",
      "id": 1,
      "name": "Spider-Man",
      "site_detail_url": "https://comicvine.gamespot.com/character/1/"
    },
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/character/500/",
      "id": 500,
      "name": "Uncle Ben",
      "site_detail_url": "https://comicvine.gamespot.com/character/500/"
    }
  ],
  "character_died_in": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/character/500/",
      "id": 500,
      "name": "Uncle Ben",
      "site_detail_url": "https://comicvine.gamespot.com/character/500/"
    }
  ],
  "concept_credits": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/concept/10/",
      "id": 10,
      "name": "Radioactive Spider",
      "site_detail_url": "https://comicvine.gamespot.com/concept/10/"
    }
  ],
  "location_credits": [],
  "object_credits": [],
  "person_credits": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/person/1/",
      "id": 1,
      "name": "Stan Lee",
      "site_detail_url": "https://comicvine.gamespot.com/person/1/"
    },
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/person/2/",
      "id": 2,
      "name": "Steve Ditko",
      "site_detail_url": "https://comicvine.gamespot.com/person/2/"
    }
  ],
  "story_arc_credits": [],
  "team_credits": [],
  "team_disbanded_in": [],
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only issues modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase creates document with 12 basic fields. Detail phase updates by ID, adding all credit arrays and full description
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Issue Model](../../issues/models.md) — PostgreSQL database model definition
- [Issues API](../../issues/api) — REST API structure