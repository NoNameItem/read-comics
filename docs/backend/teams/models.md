# Teams Models

## Summary

- `Team` — Superhero or villain team/group with member relationships

## Reference

### Team Model

Represents a comic book team or group of superheroes (e.g., "Avengers", "X-Men", "Fantastic Four"). Teams track member relationships and first appearances.

#### Database Fields

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Django primary key |
| `comicvine_id` | Integer (unique) | ComicVine API identifier |
| `name` | TextField | Team name |
| `aliases` | TextField | Pipe-separated alternative names |
| `short_description` | TextField | Short summary/deck text from ComicVine |
| `html_description` | TextField | Full HTML-formatted description |
| `thumb_url` | URLField | Thumbnail image URL (max 1000 chars) |
| `image_url` | URLField | Full-size image URL (max 1000 chars) |
| `first_issue_name` | TextField | Name of first issue featuring team |
| `first_issue` | FK → Issue | First issue featuring team (nullable, SET_NULL on delete) |
| `first_issue_comicvine_id` | Integer | ComicVine ID for first issue (used for lookup) |
| `publisher` | FK → Publisher | Team's primary publisher (nullable, CASCADE delete) |
| `slug` | AutoSlugField | URL-safe slug (unique, 1000 chars) — generated from publisher name and team name |
| `api_detail_url` | URLField | ComicVine API endpoint URL |
| `site_detail_url` | URLField | ComicVine website URL |
| `crawl_source` | CharField | Either "list" or "detail" indicating data completeness |

#### ComicVine Sync Configuration

| Setting | Value | Description |
|---|---|---|
| `MONGO_COLLECTION` | `"comicvine_teams"` | MongoDB collection name for cached ComicVine data |
| `MONGO_PROJECTION` | Excludes 11 fields | Excludes character_enemies, character_friends, characters, count_of_issue_appearances, count_of_team_members, date_added, date_last_updated, issue_credits, movies, story_arc_credits, volume_credits |
| `COMICVINE_API_URL` | Team detail endpoint | URL for fetching individual team data: `https://comicvine.gamespot.com/api/team/4060-{id}/` |
| `COMICVINE_INFO_TASK` | `team_comicvine_info_task` | Celery task for syncing from MongoDB to PostgreSQL |
| `FIELD_MAPPING` | `{"publisher": {...}}` | Maps ComicVine publisher to Django FK with `get_publisher()` method |

#### Methods

| Method | Signature | Description |
|---|---|---|
| `__str__()` | `() → str` | Returns "Team Name (Publisher Name)" or "Team Name" if no publisher |
| `get_publisher_name()` | `() → str or None` | Returns publisher name if exists, else None |
| `pre_save()` | `(force_insert, force_update, using, update_fields) → None` | On first_issue_comicvine_id change, looks up and sets first_issue FK from Issues table |
| `get_absolute_url()` | `() → str` | Returns URL for team detail view: `teams:detail` with slug |
| `get_aliases_list()` | `() → list[str]` | Returns newline-separated aliases as list, or empty list if no aliases |
| `download_link` | `@property → str` | Returns URL for team download: `teams:download` with slug |

#### Relationships

| Relation | Type | Description |
|---|---|---|
| `publisher` | ForeignKey | FK to Publisher (nullable, CASCADE delete) — team's primary publisher |
| `first_issue` | ForeignKey | FK to Issue (nullable, SET_NULL on delete) — first issue featuring this team |
| `watchers` | GenericRelation | Back-relation to WatchedItem — users can watch a team to track when issues become available |

#### Mixins

| Mixin | Provides |
|---|---|
| `ImageMixin` | `square_medium` property for image URLs in serializers; handles S3 storage for images |
| `ComicvineSyncModel` | `.sync()` method, MongoDB caching, field mapping, ComicVine API integration |

#### Model Meta

- `ordering` — By name (alphabetical)

## Details

### Team Structure

Teams allow organization of superhero/villain groups with:
- Member relationships (tracked in related issues)
- Team alliances and rivalries (from ComicVine relationships)
- Issue appearances and storylines
- Publication history through first/last issues

### First Issue Resolution

The `first_issue` field is populated automatically:
1. MongoDB contains `first_appeared_in_issue` with ComicVine ID
2. Field mapping sync extracts this as `first_issue_comicvine_id`
3. `pre_save()` hook looks up matching Issue in PostgreSQL
4. Sets `first_issue` FK if found, otherwise leaves as NULL

### Slug Generation

- Automatically generated from `[publisher_name, name]`
- Unique constraint ensures no duplicates
- Regenerates when name or publisher changes (overwrite=True)
- Custom slugify function handles special characters

### API Field Restrictions (MONGO_PROJECTION)

The following ComicVine fields are excluded from MongoDB sync:
- Character relationships: character_enemies, character_friends, characters
- Count metadata: count_of_issue_appearances, count_of_team_members
- Timestamps: date_added, date_last_updated
- Large relationships: issue_credits, movies, story_arc_credits, volume_credits

## References

- [tasks.md](tasks.md) — Celery tasks for syncing from ComicVine
- [api/serializers.md](api/serializers.md) — REST API serialization
- [api/viewsets.md](api/viewsets.md) — REST API configuration
- [search_adapters.md](search_adapters.md) — Full-text search integration
- [teams_spider.md](../spiders/teams_spider.md) — Scrapy spider for ComicVine data