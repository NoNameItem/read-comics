# Missing Issues

Tracks recently published or missing comic issues from ComicVine, supporting user notifications and collection management.

## Documentation

### Core Models
- [`models.md`](models.md) — 7 models: MissingIssue, IgnoredIssue/Volume/Publisher, APIQueue, WatchedItem, Locks

### API Layer
- [`api/endpoints.md`](api/endpoints.md) — REST endpoint specifications
- [`api/viewsets.md`](api/viewsets.md) — MissingIssueViewSet with count endpoint

### Tasks & Management
- [`tasks.md`](tasks.md) — Base missing issues task with 8 entity-specific implementations (Volume, Publisher, Character, etc.)
- [`management_commands.md`](management_commands.md) — `clearqueue` command for API queue management

### Infrastructure
- [`do_spaces.md`](do_spaces.md) — DigitalOcean Spaces integration for asset storage and browsing

## Key Features
- **Missing Issue Detection** — Identifies ComicVine issues not yet in PostgreSQL
- **Entity-Specific Tasks** — Separate Celery tasks for Volume, Character, Person, Team, etc.
- **Ignore Management** — Users can ignore specific issues, volumes, or publishers
- **Skip Logic** — Temporary skip with auto-reset after configured days
- **User Notifications** — WatchedItem integration for user tracking
- **Asset Storage** — DigitalOcean Spaces integration for missing issue metadata
- **API Queue** — Tracks entities pending synchronization
