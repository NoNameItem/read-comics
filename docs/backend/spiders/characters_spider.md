# Characters Spider

MongoDB collection: `comicvine_characters`

## Summary

Fetches comic book character data from ComicVine API. The spider performs two-phase crawling:
- **List phase**: Gets basic character information (13 fields: ID, name, image, first appearance, aliases, demographics)
- **Detail phase**: Gets comprehensive character data (22 fields: adds description, teams, relationships with other characters, creators, powers)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine character identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this character |
| `site_detail_url` | URL | ComicVine website URL for this character |
| `name` | String | Character display name |
| `aliases` | String | Pipe-separated list of alternative names and aliases |
| `deck` | String | Short summary description of the character |
| `image` | Object | Image object containing multiple URL sizes (icon, medium, screen, thumb, etc.) |
| `first_appeared_in_issue` | Reference | Issue object where character first appeared |
| `real_name` | String | Character's civilian or real name |
| `gender` | Integer | Gender code (1=Male Morph, 2=Female Morph, etc.) |
| `birth` | String | Birth date in YYYY-MM-DD format |
| `origin` | String | Origin story/background text |
| `publisher` | Reference | Publisher object (Marvel, DC, etc.) |

### Detail Endpoint Fields (adds 9 fields to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted biography and character description |
| `character_friends` | Array | Array of character objects representing allies and friends |
| `character_enemies` | Array | Array of character objects representing known enemies and adversaries |
| `teams` | Array | Array of team objects the character is/was member of |
| `team_friends` | Array | Array of team objects that are allies of this character |
| `team_enemies` | Array | Array of team objects that are enemies of this character |
| `creators` | Array | Array of person objects (writers, artists, creators) |
| `powers` | Array | Array of power objects representing abilities and superpowers |
| `count_of_issue_appearances` | Integer | Total number of issue appearances |
| `number_of_issues` | Integer | Number of issues containing this character |
| `date_added` | String | Timestamp when character was added to ComicVine |
| `date_last_updated` | String | Timestamp when character data was last updated on ComicVine |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/character/1-spider-man/",
  "site_detail_url": "https://comicvine.gamespot.com/character/1-spider-man/",
  "name": "Spider-Man",
  "aliases": "Peter Parker|Spider Man|The Amazing Spider-Man",
  "deck": "The amazing wall-crawling superhero",
  "real_name": "Peter Parker",
  "birth": "1962-06-01",
  "gender": 2,
  "origin": "Bitten by a radioactive spider while visiting the science pavilion, high school student Peter Parker was granted amazing arachnid abilities.",
  "description": "<p><strong>Spider-Man</strong> is one of Marvel's most iconic superheroes. After being bitten by a radioactive spider...</p>",
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/40/40_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/40/40_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/40/40_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/40/40_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/40/40_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/40/40_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/40/40_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/40/40_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/40/40_image.jpg"
  },
  "first_appeared_in_issue": {
    "api_detail_url": "https://comicvine.gamespot.com/api/issue/1/",
    "id": 1,
    "name": "Amazing Fantasy #15",
    "site_detail_url": "https://comicvine.gamespot.com/issue/1/"
  },
  "publisher": {
    "api_detail_url": "https://comicvine.gamespot.com/api/publisher/1/",
    "id": 1,
    "name": "Marvel",
    "site_detail_url": "https://comicvine.gamespot.com/publisher/1/"
  },
  "character_friends": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/character/2/",
      "id": 2,
      "name": "Iron Man",
      "site_detail_url": "https://comicvine.gamespot.com/character/2/"
    },
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/character/3/",
      "id": 3,
      "name": "Captain America",
      "site_detail_url": "https://comicvine.gamespot.com/character/3/"
    }
  ],
  "character_enemies": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/character/100/",
      "id": 100,
      "name": "Green Goblin",
      "site_detail_url": "https://comicvine.gamespot.com/character/100/"
    },
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/character/101/",
      "id": 101,
      "name": "Doctor Octopus",
      "site_detail_url": "https://comicvine.gamespot.com/character/101/"
    }
  ],
  "teams": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/team/1/",
      "id": 1,
      "name": "Avengers",
      "site_detail_url": "https://comicvine.gamespot.com/team/1/"
    }
  ],
  "team_friends": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/team/1/",
      "id": 1,
      "name": "Avengers",
      "site_detail_url": "https://comicvine.gamespot.com/team/1/"
    }
  ],
  "team_enemies": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/team/50/",
      "id": 50,
      "name": "Sinister Six",
      "site_detail_url": "https://comicvine.gamespot.com/team/50/"
    }
  ],
  "creators": [
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
  "powers": [
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/power/1/",
      "id": 1,
      "name": "Wall Crawling",
      "site_detail_url": "https://comicvine.gamespot.com/power/1/"
    },
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/power/2/",
      "id": 2,
      "name": "Spider Sense",
      "site_detail_url": "https://comicvine.gamespot.com/power/2/"
    },
    {
      "api_detail_url": "https://comicvine.gamespot.com/api/power/3/",
      "id": 3,
      "name": "Web Generation",
      "site_detail_url": "https://comicvine.gamespot.com/power/3/"
    }
  ],
  "count_of_issue_appearances": 2500,
  "number_of_issues": 2500,
  "date_added": "2008-06-01 00:00:00",
  "date_last_updated": "2023-01-15 12:30:45",
  "crawl_source": "detail"
}
```

## Data Sync Behavior

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` from ComicVine as filter (fetches only characters modified since last spider run)
- **Skip existing**: When `skip_existing="Y"`, middleware checks if MongoDB document has `crawl_source="detail"` already set and skips detail request to save API calls
- **Two-phase process**: List phase creates document with 13 basic fields and `crawl_source="list"`. Detail phase updates same document by ID, adding relationship fields and setting `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field — if document exists, updates it; if not, creates new

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Character Model](../../characters/models.md) — PostgreSQL database model definition
- [Characters API](../../characters/api) — REST API structure