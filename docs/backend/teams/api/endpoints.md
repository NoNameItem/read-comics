# Teams API endpoints

All endpoints are powered by [`TeamsViewSet`](viewsets.md#teamsviewset). The viewset is read-only and exposes standard list/detail operations plus a custom `count` action.

## List: `GET /api/teams/`

Returns a paginated list of comic book teams with publisher metadata and statistics. Filters out teams without matched issues by default; use `?show-all=yes` to include all records.

- **ViewSet**: [`TeamsViewSet`](viewsets.md#teamsviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`TeamsListSerializer`](serializers.md#teamslistserializer)
- **Query params**:
  - `ordering` (`name`, `issues_count`, `volumes_count`). Defaults to `name`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `show-all=yes` returns teams even if no matched issues; default is `no`, which applies `OnlyWithIssuesQuerySetMixin` filter.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "avengers",
    "image": "https://.../avengers.jpg",
    "publisher": {"name": "Marvel", "image": "https://...", "slug": "marvel"},
    "name": "Avengers",
    "short_description": "Earth's mightiest heroes.",
    "issues_count": 400,
    "volumes_count": 60
  }
  ```

## Detail: `GET /api/teams/{slug}/`

Retrieves information about a specific team. Currently returns the same fields as the list endpoint.

- **ViewSet**: [`TeamsViewSet`](viewsets.md#teamsviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`TeamsListSerializer`](serializers.md#teamslistserializer)
- **Path parameter**: `{slug}` (the slug field of the Team model).
- **Response fields**: Same as list endpoint above.

## Count: `GET /api/teams/count/`

Returns the total count of teams after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`TeamsViewSet`](viewsets.md#teamsviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (applies `OnlyWithIssuesQuerySetMixin` unless `?show-all=yes`).
- **Response**:
  ```json
  {
    "count": 95
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/teams/{slug}/` – slug-based detail endpoint expectation (`NEEDS WORK` entry).
- `GET /api/teams/{slug}/technical-info/` – return technical audit info for the team.
- `GET /api/teams/{slug}/start-watch/` – begin tracking the team.
- `GET /api/teams/{slug}/stop-watch/` – stop tracking the team.
- `GET /api/teams/{slug}/issues/{issue_slug}/` – issue detail for a team-specific issue slug.
- `GET /api/teams/{slug}/issues/` – list issues the team appears in.
- `GET /api/teams/{slug}/enemies/` – list the team's enemies.
- `GET /api/teams/{slug}/volumes/` – list volumes that featured the team.
- `GET /api/teams/{slug}/friends/` – list allied teams.
- `GET /api/teams/{slug}/characters/` – list characters affiliated with the team.
- `GET /api/teams/{slug}/disbanded-in/` – list issues in which the team disbanded.

These are `PLAN` entries in `DRF_MIGRATION_URL_MAP.md` and await slug-based detail serializers.