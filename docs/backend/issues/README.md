# Issues

Handles comic issues with numbering, release dates, downloadable files, and comprehensive metadata syncing from ComicVine.

## Documentation

### Core Models
- [`models.md`](models.md) — Issue, IssuePerson (author/editor roles), FinishedIssue (user progress tracking)

### API Layer
- [`api/endpoints.md`](api/endpoints.md) — REST endpoint specifications
- [`api/serializers.md`](api/serializers.md) — IssuesListSerializer, IssueDetailSerializer, IssueTechnicalInfoSerializer
- [`api/viewsets.md`](api/viewsets.md) — IssueViewSet with pagination, filtering, and previous/next navigation

### Search & Tasks
- [`search_adapters.md`](search_adapters.md) — Full-text search integration
- [`tasks.md`](tasks.md) — Celery tasks for ComicVine API syncing, Space file processing, and data refresh

## Key Features
- **ComicVine Integration** — Automatic field mapping and periodic sync
- **File Management** — DigitalOcean Space S3 integration for downloadable comics
- **User Progress** — Track which issues users have finished reading
- **Smart Navigation** — Previous/next issue slugs based on current sorting
- **Flexible Sorting** — Multi-field ordering by volume, number, cover date
