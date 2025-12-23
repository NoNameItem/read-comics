# Story Arcs Module

Comic book story arcs represent multi-issue narrative arcs or storylines (e.g., "The Dark Phoenix Saga", "Infinity Gauntlet"). Story arcs help users follow complex narratives that span multiple issues across various volumes.

## Documentation

- [models.md](models.md) — StoryArc database model, fields, ComicVine sync configuration
- [api/serializers.md](api/serializers.md) — REST API serializers (StoryArcsListSerializer, StartedStoryArcSerializer)
- [api/viewsets.md](api/viewsets.md) — REST API ViewSet with list, started, and count endpoints
- [search_adapters.md](search_adapters.md) — Full-text search integration
- [tasks.md](tasks.md) — Celery tasks for ComicVine sync and spider execution

## Key Features

- **User Tracking**: Users can watch story arcs and track reading progress
- **Multi-Volume Coverage**: Story arcs span multiple volumes and publishers
- **Progress Tracking**: API shows how many issues in each arc user has completed
- **Search Integration**: Full-text search across story arc data
- **Incremental Sync**: Efficient ComicVine API sync with incremental and skip-existing modes

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/story-arcs/` | GET | List all story arcs with counts and progress |
| `/api/story-arcs/count/` | GET | Get total story arc count |
| `/api/story-arcs/started/` | GET | Get user's in-progress story arcs |

Query parameters:
- `ordering` — Sort by: name, issues_count, volumes_count
- `hide_finished` — Set to "true" to exclude completed story arcs
- `page`, `page_size` — Pagination (default page_size: 20)

## Data Model

```
StoryArc
├── name (TextField)
├── aliases (TextField)
├── short_description (TextField)
├── html_description (TextField)
├── publisher (FK → Publisher)
├── first_issue (FK → Issue)
├── first_issue_comicvine_id (Integer)
├── thumb_url (URLField)
├── image_url (URLField)
├── slug (AutoSlugField, unique)
└── watchers (GenericRelation → WatchedItem)
```

## Relationships

- **Publisher**: Story arc's primary publisher (optional)
- **First Issue**: First issue in the story arc (resolved from ComicVine ID on sync)
- **Watchers**: Users can watch a story arc to track when issues become available
- **Issues**: Associated via issue model (not direct FK, but linked through issue data)

## ComicVine Integration

- **MongoDB Collection**: `comicvine_story_arcs`
- **ComicVine Endpoint**: `https://comicvine.gamespot.com/api/story_arc/4045-{id}/`
- **Force Detail**: `True` — Always fetch full data, no list-only mode
- **Excluded Fields**: episodes, first_appeared_in_episode, issues, movies, count_of_issue_appearances, date_added, date_last_updated

## Syncing Process

1. **Spider Execution** — StoryArcsSpider fetches story arc data from ComicVine API
2. **MongoDB Storage** — Raw JSON data stored in `comicvine_story_arcs` collection
3. **Task Trigger** — MongoPipeline triggers `StoryArcComicvineInfoTask`
4. **PostgreSQL Sync** — Field mapping applied, FKs resolved, record created/updated
5. **Missing Issues** — StoryArcMissingIssuesTask queued to detect gaps in each arc

## Usage

### Browsing Story Arcs

```
GET /api/story-arcs/?ordering=name&page=1
```

Returns paginated list with story arc metadata including:
- Name, publisher, image
- Issue count, completed issue count
- Whether arc is finished by current user

### Tracking Progress

```
GET /api/story-arcs/started/
```

Returns story arcs user has started reading with:
- Progress (finished_count / issues_count)
- Date of most recent completion
- Sorted by recency

### Filtering

```
GET /api/story-arcs/?hide_finished=true
```

Excludes story arcs user has completely finished reading.

## Admin Operations

### Manual Full Refresh

```python
from read_comics.story_arcs.tasks import story_arcs_refresh_task
story_arcs_refresh_task.delay()
```

### Incremental Update (Recommended)

```python
from read_comics.story_arcs.tasks import story_arcs_skip_existing_increment_update
story_arcs_skip_existing_increment_update.delay()
```

### Inspect MongoDB Data

```python
from read_comics.spiders.mongo_connection import Connect
db = Connect.get_connection()
arc = db.comicvine_story_arcs.find_one({"id": 4045})
print(arc)
```
