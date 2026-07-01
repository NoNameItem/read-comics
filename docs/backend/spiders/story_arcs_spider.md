# Story Arcs Spider

MongoDB collection: `comicvine_story_arcs`

## Summary

Fetches comic book story arc data from ComicVine API. Story arcs represent multi-issue storylines or narrative arcs (e.g., "The Dark Phoenix Saga", "Infinity Gauntlet").

- **List phase**: Gets basic story arc information (9 fields: ID, name, image, first appearance, aliases, publisher, deck)
- **Detail phase**: Gets complete story arc data (10 fields: adds full description)

## API Fields

### List Endpoint Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer | ComicVine story arc identifier |
| `api_detail_url` | URL | ComicVine API endpoint for this story arc |
| `site_detail_url` | URL | ComicVine website URL for this story arc |
| `name` | String | Story arc name/title |
| `aliases` | String | Pipe-separated list of alternative names |
| `deck` | String | Short summary description of the story arc |
| `image` | Object | Image object containing multiple URL sizes |
| `first_appeared_in_issue` | Reference | Issue object where story arc began |
| `publisher` | Reference | Publisher object associated with this story arc |

### Detail Endpoint Fields (adds 1 field to list fields)

| Field Name | Type | Description |
|---|---|---|
| `description` | String | Full HTML-formatted description of the story arc |

## MongoDB Document Structure

Example document with all list and detail fields:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439019"),
  "id": 1,
  "api_detail_url": "https://comicvine.gamespot.com/api/story-arc/1-the-dark-phoenix-saga/",
  "site_detail_url": "https://comicvine.gamespot.com/story-arc/1-the-dark-phoenix-saga/",
  "name": "The Dark Phoenix Saga",
  "aliases": "Dark Phoenix|Phoenix Saga",
  "deck": "Classic X-Men storyline featuring Jean Grey and the Phoenix Force",
  "description": "<p><strong>The Dark Phoenix Saga</strong> is one of the most famous X-Men storylines. It features the corruption of Jean Grey by the Phoenix Force and culminates in her apparent death. The storyline is considered a masterpiece of superhero storytelling...</p>",
  "image": {
    "icon_url": "https://comicvine.gamespot.com/a/uploads/square_avatar/0/1/storyarc_avatar.jpg",
    "medium_url": "https://comicvine.gamespot.com/a/uploads/scale_medium/0/1/storyarc_image.jpg",
    "screen_url": "https://comicvine.gamespot.com/a/uploads/screen_medium/0/1/storyarc_image.jpg",
    "screen_large_url": "https://comicvine.gamespot.com/a/uploads/screen_large/0/1/storyarc_image.jpg",
    "small_url": "https://comicvine.gamespot.com/a/uploads/scale_small/0/1/storyarc_image.jpg",
    "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/1/storyarc_image.jpg",
    "thumb_url": "https://comicvine.gamespot.com/a/uploads/scale_thumb/0/1/storyarc_image.jpg",
    "tiny_url": "https://comicvine.gamespot.com/a/uploads/scale_tiny/0/1/storyarc_image.jpg",
    "original_url": "https://comicvine.gamespot.com/a/uploads/original/0/1/storyarc_image.jpg"
  },
  "first_appeared_in_issue": {
    "api_detail_url": "https://comicvine.gamespot.com/api/issue/500/",
    "id": 500,
    "name": "The Uncanny X-Men #101",
    "site_detail_url": "https://comicvine.gamespot.com/issue/500/"
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

- **Incremental sync**: When `incremental="Y"`, spider uses `date_last_updated` filter to fetch only story arcs modified since last run
- **Skip existing**: When `skip_existing="Y"`, skips detail request if document has `crawl_source="detail"`
- **Two-phase process**: List phase sets `crawl_source="list"`. Detail phase updates by ID with description and sets `crawl_source="detail"`
- **MongoDB storage**: Upserts by ID field

## References

- [base_spider.md](base_spider.md) — Common BaseSpider configuration and behavior
- [Story Arc Model](../../story_arcs/models.md) — PostgreSQL database model definition
- [Story Arcs API](../../story_arcs/api) — REST API structure