# Volumes Models

## Summary

- `Volume` — Comic book series/collection with issue ranges and publication metadata

## Reference

### Volume Model

Represents a comic book series or volume (e.g., "The Amazing Spider-Man", "X-Men"). Tracks first/last issues, publication year, and reading progress.

#### Database Fields

**Inherited from ComicvineSyncModel:**

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Django primary key |
| `comicvine_id` | Integer (unique) | ComicVine API identifier |
| `api_detail_url` | URLField | ComicVine API endpoint URL |
| `site_detail_url` | URLField | ComicVine website URL |
| `crawl_source` | CharField | Either "list" or "detail" indicating data completeness |

**Custom Fields (defined in Volume model):**

| Field Name | Type | Description |
|---|---|---|
| `name` | TextField | Series/volume name |
| `aliases` | TextField | Pipe-separated alternative names (nullable) |
| `short_description` | TextField | Short summary/deck from ComicVine (nullable) |
| `html_description` | TextField | Full HTML-formatted description (nullable) |
| `start_year` | IntegerField | Year series started (nullable) |
| `thumb_url` | URLField | Thumbnail image URL (max 1000 chars, nullable) |
| `image_url` | URLField | Full-size image URL (max 1000 chars, nullable) |
| `first_issue_name` | TextField | Name of first issue (nullable) |
| `first_issue` | FK → Issue | First issue in series (nullable, SET_NULL on delete) |
| `first_issue_comicvine_id` | Integer | ComicVine ID for first issue (nullable) |
| `first_issue_number` | CharField | Number/identifier of first issue (max 10 chars, nullable) |
| `last_issue_name` | TextField | Name of last issue (nullable) |
| `last_issue` | FK → Issue | Last/most recent issue (nullable, SET_NULL on delete) |
| `last_issue_comicvine_id` | Integer | ComicVine ID for last issue (nullable) |
| `last_issue_number` | CharField | Number/identifier of last issue (max 100 chars, nullable) |
| `publisher` | FK → Publisher | Series publisher (nullable, CASCADE delete) |
| `slug` | AutoSlugField | URL-safe slug (unique, 1000 chars) — generated from publisher, name, and start_year |

#### ComicVine Sync Configuration

| Setting | Value | Description |
|---|---|---|
| `MONGO_COLLECTION` | `"comicvine_volumes"` | MongoDB collection name for cached ComicVine data |
| `MONGO_PROJECTION` | Excludes 9 fields | Excludes characters, concepts, count_of_issues, date_added, date_last_updated, issue_credits, locations, objects, people |
| `COMICVINE_API_URL` | Volume detail endpoint | URL for fetching individual volume data: `https://comicvine.gamespot.com/api/volume/4050-{id}/` |
| `COMICVINE_FORCE_DETAIL_INFO` | `True` | Always fetch full detail data (no list-only mode) |
| `FIELD_MAPPING` | Complex mapping (7 fields) | Maps ComicVine fields to Django fields with custom methods for issue lookup and year conversion |
| `COMICVINE_INFO_TASK` | `volume_comicvine_info_task` | Celery task for syncing from MongoDB to PostgreSQL |

#### Field Mapping Detail

Complex FIELD_MAPPING with custom methods:

| Target Field | Source | Method | Description |
|---|---|---|---|
| `publisher` | publisher | get_publisher | Maps ComicVine publisher to Django FK |
| `first_issue_name` | first_issue.id | get_issue_name | Extracts name from issue ID |
| `first_issue` | first_issue.id | get_issue | Looks up Issue FK from ComicVine ID |
| `first_issue_comicvine_id` | first_issue.id | (direct) | Direct mapping of ComicVine issue ID |
| `first_issue_number` | first_issue.issue_number | (direct) | Direct mapping of issue number |
| `last_issue_name` | last_issue.id | get_issue_name | Extracts name from issue ID |
| `last_issue` | last_issue.id | get_issue | Looks up Issue FK from ComicVine ID |
| `last_issue_comicvine_id` | last_issue.id | (direct) | Direct mapping of ComicVine issue ID |
| `last_issue_number` | last_issue.issue_number | (direct) | Direct mapping of issue number |
| `start_year` | start_year | to_int | Converts string year to integer |

#### Methods

| Method | Signature | Description |
|---|---|---|
| `__str__()` | `() → str` | Returns "Name (start_year) (Publisher)" format with fallback to "Unknown" for missing parts |
| `get_publisher_name()` | `() → str or None` | Returns publisher name if exists, else None |
| `get_absolute_url()` | `() → str` | Returns URL for volume detail view: `volumes:detail` with slug |
| `download_link` | `@property → str` | Returns URL for volume download: `volumes:download` with slug |
| `full_name` | `@property → str` | Returns "[Publisher] Name (year)" format for display |
| `display_name` | `@property → str` | Returns "Name (year or 'Unknown')" for UI display |
| `real_last_issue_number` | `@property → str or None` | Gets actual last issue number from related issues ordered by numerical_number/number |
| `pre_save()` | `(force_insert, force_update, using, update_fields) → None` | On first/last issue comicvine_id change, looks up and sets FK from Issues table; updates issue metadata on name/year change |
| `post_save()` | `() → None` | Deletes IgnoredVolume and IgnoredIssue records to allow re-import |
| `update_issues_do_metadata()` | `() → None` | Updates do_metadata field on all related issues with volume name and year |
| `to_int()` | `@staticmethod (val) → int or None` | Safely converts value to integer, returns None on ValueError |

#### Relationships

| Relation | Type | Description |
|---|---|---|
| `publisher` | ForeignKey | FK to Publisher (nullable, CASCADE delete) — volume's publisher |
| `first_issue` | ForeignKey | FK to Issue (nullable, SET_NULL on delete) — first issue in series |
| `last_issue` | ForeignKey | FK to Issue (nullable, SET_NULL on delete) — last/most recent issue |
| `watchers` | GenericRelation | Back-relation to WatchedItem — users can watch a volume |
| `issues` (reverse) | Reverse FK | Related Issue objects in this volume |

#### Mixins

| Mixin | Provides |
|---|---|
| `ImageMixin` | `square_medium` property for image URLs in serializers; S3 storage handling |
| `DownloadSizeMixin` | Methods for computing download sizes of related issues |
| `AliasesListMixin` | Helper methods for parsing aliases |
| `ComicvineSyncModel` | `.sync()` method, MongoDB caching, field mapping, ComicVine API integration |

#### Model Meta

- `ordering` — By (name, start_year) alphabetically by name then year

## Details

### Volume Structure

Volumes organize comic issues by series with:
- First and last issue tracking
- Publisher affiliation
- Publication year range
- User reading progress tracking

### Complex Field Mapping

Volume uses complex FIELD_MAPPING for ComicVine sync:
1. `first_issue.id` extracts ComicVine issue ID
2. Custom `get_issue()` method looks up matching PostgreSQL Issue
3. Similar logic for last issue
4. `to_int()` safely converts start_year

This allows ComicVine relationship objects to be resolved to PostgreSQL ForeignKeys.

### First/Last Issue Resolution

On pre_save():
1. Detects change in `first_issue_comicvine_id`
2. Queries Issues table for matching comicvine_id
3. Sets `first_issue` FK if found, else NULL
4. Same logic for `last_issue_comicvine_id`

### Issue Metadata Updates

When volume name or start_year changes:
1. `pre_save()` calls `update_issues_do_metadata()`
2. Updates `do_metadata` field on all related issues
3. Tracks volume name and year for display in issue detail

### Post-Save Cleanup

On `post_save()`:
1. Deletes any IgnoredVolume records for this volume
2. Deletes any IgnoredIssue records for this volume
3. Allows user to re-import previously ignored items

### Slug Generation

- Auto-generated from `[publisher_name, name, start_year]`
- Unique constraint ensures no duplicates
- Regenerates when inputs change (overwrite=True)
- Custom slugify function handles special characters

### API Field Restrictions (MONGO_PROJECTION)

The following ComicVine fields excluded from MongoDB sync:
- Relationship arrays: characters, concepts, locations, objects, people
- Count metadata: count_of_issues
- Timestamps: date_added, date_last_updated
- Credits: issue_credits

### Real Last Issue Logic

`real_last_issue_number` property:
1. Queries related issues ordered by numerical_number (numeric sort) then number (string fallback)
2. Gets most recent issue number
3. Falls back to `last_issue.number` if no related issues found
4. Returns None if neither available

## References

- [tasks.md](tasks.md) — Celery tasks for ComicVine sync and space import
- [api/serializers.md](api/serializers.md) — REST API serialization
- [api/viewsets.md](api/viewsets.md) — REST API configuration and mixins
- [search_adapters.md](search_adapters.md) — Full-text search integration
- [volumes_spider.md](../spiders/volumes_spider.md) — Scrapy spider for ComicVine data