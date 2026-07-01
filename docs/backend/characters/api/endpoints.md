# Characters API endpoints

All endpoints are powered by [`CharacterViewSet`](viewsets.md#characterviewset). The viewset is read-only and exposes standard list/detail operations plus custom `count` and `technical-info` actions.

## List: `GET /api/characters/`

Returns a paginated list of comic book characters with compact metadata. Filters out characters without matched issues by default; use `?show-all=yes` to include all records.

- **ViewSet**: [`CharacterViewSet`](viewsets.md#characterviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`CharactersListSerializer`](serializers.md#characterslistserializer)
- **Query params**:
  - `ordering` (`name`, `issues_count`, `volumes_count`). Defaults to `name`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `show-all=yes` returns characters even if no matched issues; default is `no`, which applies `OnlyWithIssuesQuerySetMixin` filter.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "superman",
    "image": "https://.../superman.jpg",
    "publisher": {"name": "DC", "image": "https://...", "slug": "dc"},
    "name": "Superman",
    "short_description": "The Man of Steel.",
    "issues_count": 42,
    "volumes_count": 5
  }
  ```

## Detail: `GET /api/characters/{slug}/`

Retrieves comprehensive information about a specific character including aliases, abilities, first appearance, and download metadata. Lookup is by URL-safe slug identifier.

- **ViewSet**: [`CharacterViewSet`](viewsets.md#characterviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`CharacterDetailSerializer`](serializers.md#characterdetailserializer)
- **Path parameter**: `{slug}` (the slug field of [`Character`](../models.md#character) model).
- **Response fields** include slug, name, real name, full and square images, publisher metadata, list of aliases, birth date, gender (display string), powers, first issue name/slug, ComicVine URL, short description, full description, and download links/sizes. Example:
  ```json
  {
    "slug": "batman",
    "name": "Batman",
    "real_name": "Bruce Wayne",
    "image": "https://.../batman.png",
    "square_image": "https://.../batman_square.png",
    "publisher": {"name": "DC", "image": "https://...", "slug": "dc"},
    "aliases": ["The Dark Knight"],
    "birth": "1939-05-01",
    "gender": "Male",
    "powers": ["Stealth", "Detective"],
    "first_issue_name": "Detective Comics #27",
    "first_issue_slug": "detective-comics-27",
    "comicvine_url": "https://comicvine.gamespot.com/batman/4005-120/",
    "short_description": "Gotham's vigilante.",
    "description": "Long form character history...",
    "download_link": "https://example.com/download/batman.zip",
    "download_size": "256 MB"
  }
  ```

## Count: `GET /api/characters/count/`

Returns the total count of characters after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`CharacterViewSet`](viewsets.md#characterviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (applies `OnlyWithIssuesQuerySetMixin` unless `?show-all=yes`).
- **Response**:
  ```json
  {
    "count": 123
  }
  ```

## Technical Info: `GET /api/characters/{slug}/technical-info/`

Exposes administrative metadata about ComicVine synchronization status for the character. Restricted to staff and superuser access only.

- **ViewSet**: [`CharacterViewSet`](viewsets.md#characterviewset)
- **Action**: `technical_info` (from `TechnicalInfoActionMixin`)
- **Serializer**: [`CharacterTechnicalInfoSerializer`](serializers.md#charactertechnicalinfoserializer)
- **Path parameter**: `{slug}` (the slug field of [`Character`](../models.md#character) model).
- **Permissions**: `IsSuperuserOrStaff` only.
- **Response**:
  ```json
  {
    "id": 1,
    "comicvine_id": 12345,
    "comicvine_status": "Matched",
    "comicvine_last_match": "2025-12-22T12:00:00Z",
    "created_dt": "2020-01-01T00:00:00Z",
    "modified_dt": "2025-12-22T00:00:00Z"
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/characters/{slug}/start-watch/` – mark a character as watched for the requesting user (mirrors `<slug>/start_watch/`).
- `GET /api/characters/{slug}/stop-watch/` – remove the watch flag for the character.
- `GET /api/characters/{slug}/issues/` – list issues featuring the character.
- `GET /api/characters/{slug}/volumes/` – list volumes that include the character.
- `GET /api/characters/{slug}/died-in-issues/` – list issues where the character died.
- `GET /api/characters/{slug}/enemies/` – list the character's enemies.
- `GET /api/characters/{slug}/friends/` – list the character's friends.
- `GET /api/characters/{slug}/teams/` – list teams the character belongs to.
- `GET /api/characters/{slug}/team-friends/` – list friends from shared teams.
- `GET /api/characters/{slug}/team-enemies/` – list enemies that arise from shared teams.
- `GET /api/characters/{slug}/authors/` – list creators associated with the character.
- `GET /api/characters/{slug}/issues/{issue_slug}/` – details for a specific issue slug scoped to the character.

Each is flagged `PLAN` in `DRF_MIGRATION_URL_MAP.md` and will reuse slug lookups once implemented.