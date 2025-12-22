# Teams API endpoints

`TeamsViewSet` exposes `/api/teams/` and the shared `count` action.

## List: `GET /api/teams/`
- **Action**: `list`
- **Query params**: `ordering` (`name`,`issues_count`,`volumes_count`), `show-all=yes`, pagination.
- **Response sample**:
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
- **Action**: `retrieve`
- **Response**: same fields as the list serializer.

## `count`: `GET /api/teams/count/`
Reports the filtered total.

## Input payloads
Only GET endpoints exist.

## Planned DRF endpoints (status PLAN)
- `GET /api/teams/{slug}/` – slug-based detail endpoint expectation (`NEEDS WORK` entry).
- `GET /api/teams/{slug}/technical-info/` – return technical audit info for the team.
- `GET /api/teams/{slug}/start-watch/` – begin tracking the team.
- `GET /api/teams/{slug}/stop-watch/` – stop tracking the team.
- `GET /api/teams/{slug}/issues/{issue_slug}/` – issue detail for a team-specific issue slug.
- `GET /api/teams/{slug}/issues/` – list issues the team appears in.
- `GET /api/teams/{slug}/enemies/` – list the team’s enemies.
- `GET /api/teams/{slug}/volumes/` – list volumes that featured the team.
- `GET /api/teams/{slug}/friends/` – list allied teams.
- `GET /api/teams/{slug}/characters/` – list characters affiliated with the team.
- `GET /api/teams/{slug}/disbanded-in/` – list issues in which the team disbanded.

These are `PLAN` entries in `DRF_MIGRATION_URL_MAP.md` and await slug-based detail serializers.
