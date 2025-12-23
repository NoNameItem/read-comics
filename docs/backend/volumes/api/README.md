# Volumes API

REST API for browsing comic volumes and tracking reading progress.

## Documentation

- [serializers.md](serializers.md) — Volume serializers (nested, list, started)
- [viewsets.md](viewsets.md) — VolumesViewSet with list, started, and count endpoints

## Quick Reference

| Endpoint | Methods | Description |
|---|---|---|
| `/api/volumes/` | GET | List volumes with pagination and filtering |
| `/api/volumes/count/` | GET | Total count of volumes |
| `/api/volumes/started/` | GET | User's in-progress volumes |

Query parameters:
- `ordering` — Sort field: start_year (default), name, issues_count
- `hide_finished` — Hide completed volumes: "true"
- `page`, `page_size` — Pagination (default page_size: 20)
