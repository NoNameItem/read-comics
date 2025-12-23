# Story Arcs API

REST API for browsing story arcs and tracking reading progress.

## Documentation

- [serializers.md](serializers.md) — StoryArcsListSerializer, StartedStoryArcSerializer
- [viewsets.md](viewsets.md) — StoryArcsViewSet with list, started, and count endpoints

## Quick Reference

| Endpoint | Methods | Description |
|---|---|---|
| `/api/story-arcs/` | GET | List story arcs with pagination |
| `/api/story-arcs/count/` | GET | Total count of story arcs |
| `/api/story-arcs/started/` | GET | User's started story arcs |

Query parameters:
- `ordering` — Sort field: name (default), issues_count, volumes_count
- `hide_finished` — Hide completed arcs: "true"
