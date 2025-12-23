# Story Arcs Models

## Summary

- `StoryArc` — Multi-issue comic book storyline or narrative arc

## Reference

### StoryArc Model

Represents a comic book story arc or multi-issue storyline (e.g., "The Dark Phoenix Saga", "Infinity Gauntlet"). Story arcs group related issues across volumes and track user progress through multi-issue stories.

**Inherited Fields from ComicvineSyncModel:**

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Django primary key |
| `comicvine_id` | Integer (unique) | ComicVine API identifier |
| `api_detail_url` | URLField | ComicVine API endpoint URL |
| `site_detail_url` | URLField | ComicVine website URL |
| `crawl_source` | CharField | Either "list" or "detail" indicating data completeness |
| `comicvine_status` | CharField | Status: Not Matched, Queued, or Matched |
| `comicvine_last_match` | DateTimeField | Timestamp of last successful sync |
| `created_dt` | DateTimeField | Record creation timestamp (auto-set) |
| `modified_dt` | DateTimeField | Last modification timestamp (auto-updated) |

**Custom Fields (defined in StoryArc model):**

| Field Name | Type | Description |
|---|---|---|
| `name` | TextField | Story arc title/name |
| `aliases` | TextField | Pipe-separated alternative names |
| `short_description` | TextField | Short summary/deck text from ComicVine |
| `html_description` | TextField | Full HTML-formatted description |
| `thumb_url` | URLField | Thumbnail image URL (max 1000 chars) |
| `image_url` | URLField | Full-size image URL (max 1000 chars) |
| `publisher` | FK → Publisher | Publisher of this story arc (nullable) |
| `first_issue_name` | TextField | Name of the first issue in the arc |
| `first_issue` | FK → Issue | First issue in the arc (nullable, SET_NULL on delete) |
| `first_issue_comicvine_id` | Integer | ComicVine ID for first issue (used for lookup) |
| `slug` | AutoSlugField | URL-safe slug (unique, 1000 chars) — generated from publisher name and story arc name |
| `watchers` | GenericRelation → WatchedItem | Users watching this story arc |
| `tracker` | FieldTracker | Tracks field changes for synchronization |

#### ComicVine Sync Configuration

| Setting | Value | Description |
|---|---|---|
| `MONGO_COLLECTION` | `"comicvine_story_arcs"` | MongoDB collection name for cached ComicVine data |
| `MONGO_PROJECTION` | Excludes 7 fields | Excludes count_of_issue_appearances, date_added, date_last_updated, episodes, first_appeared_in_episode, issues, movies from MongoDB sync |
| `COMICVINE_API_URL` | Story arc detail endpoint | URL for fetching individual story arc data: `https://comicvine.gamespot.com/api/story_arc/4045-{id}/` |
| `COMICVINE_FORCE_DETAIL_INFO` | `True` | Always fetch full detail data (no list-only mode) |
| `COMICVINE_INFO_TASK` | `story_arc_comicvine_info_task` | Celery task for syncing from MongoDB to PostgreSQL |
| `FIELD_MAPPING` | `{"publisher": {...}}` | Maps ComicVine publisher to Django FK with `get_publisher()` method |

#### Methods

| Method | Signature | Description |
|---|---|---|
| `__str__()` | `() → str` | Returns "Story Arc Name (Publisher Name)" or "Story Arc Name" if no publisher |
| `get_publisher_name()` | `() → str or None` | Returns publisher name if exists, else None |
| `pre_save()` | `(force_insert, force_update, using, update_fields) → None` | On first_issue_comicvine_id change, looks up and sets first_issue FK from Issues table |
| `get_absolute_url()` | `() → str` | Returns URL for story arc detail view: `story_arcs:detail` with slug |
| `download_link` | `@property → str` | Returns URL for story arc download: `story_arcs:download` with slug |
| `get_aliases_list()` | `() → list[str]` | Returns newline-separated aliases as list, or empty list if no aliases |

#### Relationships

| Relation | Type | Description |
|---|---|---|
| `publisher` | ForeignKey | FK to Publisher (nullable, CASCADE delete) — story arc's primary publisher |
| `first_issue` | ForeignKey | FK to Issue (nullable, SET_NULL on delete) — first issue in the arc |
| `watchers` | GenericRelation | Back-relation to WatchedItem — users can watch a story arc to track when issues become available |

#### Mixins

| Mixin | Provides |
|---|---|
| `ImageMixin` | `square_medium` property for image URLs in serializers; handles S3 storage for images |
| `ComicvineSyncModel` | `.sync()` method, MongoDB caching, field mapping, ComicVine API integration |

#### Model Meta

- `ordering` — By name (alphabetical)

## Details

### Story Arc Tracking

Story arcs allow users to follow multi-issue narrative arcs:
- User can watch a story arc via `watchers` relation
- When issues in the arc become available, they're associated with the story arc
- Missing issues tracking includes story arc mapping to identify gaps

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
- `count_of_issue_appearances` — Count metadata (computed in QuerySet mixin)
- `date_added`, `date_last_updated` — Timestamps not needed for display
- `episodes`, `first_appeared_in_episode` — TV episode references (unused)
- `issues`, `movies` — Large relationship arrays (fetched separately via API)

## References

- [tasks.md](tasks.md) — Celery tasks for syncing from ComicVine
- [api/serializers.md](api/serializers.md) — REST API serialization
- [api/viewsets.md](api/viewsets.md) — REST API configuration
- [search_adapters.md](search_adapters.md) — Full-text search integration
- [story_arcs_spider.md](../spiders/story_arcs_spider.md) — Scrapy spider for ComicVine data