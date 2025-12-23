# Teams Module

Superhero and villain teams/groups with member relationships and appearance tracking.

## Documentation

- [models.md](models.md) — Team database model, fields, ComicVine sync configuration
- [api/serializers.md](api/serializers.md) — REST API serializers (TeamsListSerializer)
- [api/viewsets.md](api/viewsets.md) — REST API ViewSet with list and count endpoints
- [search_adapters.md](search_adapters.md) — Full-text search integration
- [tasks.md](tasks.md) — Celery tasks for ComicVine sync and spider execution

## Key Features

- **Team Tracking**: Browse and search superhero/villain teams
- **Issue Appearance**: See which issues feature each team
- **Publisher Grouping**: Teams organized by publisher
- **Search Integration**: Full-text search across team data
- **Incremental Sync**: Efficient ComicVine API sync

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/teams/` | GET | List all teams with counts |
| `/api/teams/count/` | GET | Get total team count |

Query parameters:
- `ordering` — Sort by: name, issues_count, volumes_count
- `page`, `page_size` — Pagination

## Data Model

```
Team
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

## ComicVine Integration

- **MongoDB Collection**: `comicvine_teams`
- **ComicVine Endpoint**: `https://comicvine.gamespot.com/api/team/4060-{id}/`
- **Excluded Fields**: character relationships, count fields, timestamps, large relationship arrays
