# Volumes Module

Comic book series/volumes with issue ranges, publication metadata, and reading progress tracking.

## Documentation

- [models.md](models.md) — Volume model with complex field mapping and sync configuration
- [api/serializers.md](api/serializers.md) — REST API serializers (nested, list, started)
- [api/viewsets.md](api/viewsets.md) — REST API ViewSet with list, started, and count endpoints
- [search_adapters.md](search_adapters.md) — Full-text search integration with custom title formatting
- [tasks.md](tasks.md) — Celery tasks for ComicVine sync, S3 processing, and spider execution

## Key Features

- **Series Management**: Track comic book series with first/last issue references
- **Publication Metadata**: Year, publisher, aliases tracking
- **Reading Progress**: Track finished issues, completion status, reading speed
- **S3 Integration**: Process volume directories from DigitalOcean Spaces
- **Search**: Full-text search with publication year in results
- **Incremental Sync**: Efficient ComicVine API sync strategies

## Data Model

```
Volume
├── name (TextField)
├── aliases (TextField)
├── short_description (TextField)
├── html_description (TextField)
├── start_year (IntegerField)
├── first_issue (FK → Issue)
├── last_issue (FK → Issue)
├── publisher (FK → Publisher)
├── thumb_url (URLField)
├── image_url (URLField)
├── slug (AutoSlugField, unique)
└── watchers (GenericRelation → WatchedItem)
```

## Relationships

- **Publisher**: Series publisher (nullable, CASCADE delete)
- **First Issue**: First issue in series (nullable, SET_NULL on delete)
- **Last Issue**: Last/most recent issue (nullable, SET_NULL on delete)
- **Watchers**: Users watching this volume
- **Issues** (reverse): Issues in this volume

## ComicVine Integration

- **MongoDB Collection**: `comicvine_volumes`
- **ComicVine Endpoint**: `https://comicvine.gamespot.com/api/volume/4050-{id}/`
- **Force Detail**: `True` — Always fetch full data
- **Excluded Fields**: characters, concepts, locations, objects, people, count_of_issues, timestamps, issue_credits

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/volumes/` | GET | List all volumes with counts and progress |
| `/api/volumes/count/` | GET | Get total volume count |
| `/api/volumes/started/` | GET | Get user's in-progress volumes |

## Task Processing Pipeline

1. **Spider Execution** — VolumesSpider fetches from ComicVine API
2. **MongoDB Storage** — Raw JSON stored in `comicvine_volumes` collection
3. **Celery Task** — VolumeComicvineInfoTask syncs to PostgreSQL
4. **Field Mapping** — Complex mapping resolves ComicVine relationships to Django FKs
5. **Post-Save** — Deletes ignored records, updates issue metadata
6. **Missing Issues** — VolumeMissingIssuesTask detects gaps
7. **Space Processing** — VolumeProcessEntryTask handles S3 directories

## Search Features

Volumes searchable by:
- Name
- Aliases
- Short description
- HTML description
- Custom title (includes year and aliases)

Search results show: "Name Year\nAliases" for improved discovery
