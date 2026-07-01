# Teams API

REST API for browsing superhero and villain teams.

## Documentation

- [serializers.md](serializers.md) — TeamsListSerializer
- [viewsets.md](viewsets.md) — TeamsViewSet with list and count endpoints

## Quick Reference

| Endpoint | Methods | Description |
|---|---|---|
| `/api/teams/` | GET | List teams with pagination |
| `/api/teams/count/` | GET | Total count of teams |

Query parameters:
- `ordering` — Sort field: name (default), issues_count, volumes_count