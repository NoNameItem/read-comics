# Story arcs API endpoints

All endpoints are powered by [`StoryArcsViewSet`](viewsets.md#storyarcsviewset). The viewset is read-only and exposes standard list/detail operations plus custom `count` and `started` actions with filtering for finished state.

## List: `GET /api/story-arcs/`

Returns a paginated list of comic book story arcs with publisher metadata and reading progress annotations. Supports filtering by finished status and issue count.

- **ViewSet**: [`StoryArcsViewSet`](viewsets.md#storyarcsviewset)
- **Action**: `list` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`StoryArcsListSerializer`](serializers.md#storyarcslistserializer)
- **Query params**:
  - `ordering` (`name`, `issues_count`, `volumes_count`). Defaults to `name`. The `UniqueOrderingFilter` always appends `id` so pagination stays stable.
  - `show-all=yes` bypasses the default `issues_count > 0` policy.
  - `hide-finished=yes` (default) filters out arcs where the current user finished every issue; set `hide-finished=no` to include completed arcs.
  - DRF pagination params (`page`, `page_size`).
- **Response structure**: paginated dict with `count`, `next`, `previous`, `results`. Each entry contains:
  ```json
  {
    "slug": "infinity-gauntlet",
    "image": "https://.../gauntlet.jpg",
    "publisher": {"name": "Marvel", "image": "https://...", "slug": "marvel"},
    "name": "Infinity Gauntlet",
    "short_description": "The cosmic gauntlet event.",
    "issues_count": 6,
    "finished_count": 1,
    "volumes_count": 2,
    "is_finished": false
  }
  ```

## Detail: `GET /api/story-arcs/{slug}/`

Retrieves information about a specific story arc. Currently returns the same fields as the list endpoint.

- **ViewSet**: [`StoryArcsViewSet`](viewsets.md#storyarcsviewset)
- **Action**: `retrieve` (inherited from `ReadOnlyModelViewSet`)
- **Serializer**: [`StoryArcsListSerializer`](serializers.md#storyarcslistserializer)
- **Path parameter**: `{slug}` (the slug field of the StoryArc model).
- **Response fields**: Same as list endpoint above.

## Count: `GET /api/story-arcs/count/`

Returns the total count of story arcs after applying active filters. Useful for dashboard widgets and sidebar badges.

- **ViewSet**: [`StoryArcsViewSet`](viewsets.md#storyarcsviewset)
- **Action**: `count` (from `CountActionMixin`)
- **Serializer**: None (returns plain JSON object)
- **Query params**: Respects the same filters as `list` (`hide-finished`, `show-all`).
- **Response**:
  ```json
  {
    "count": 78
  }
  ```

## Started: `GET /api/story-arcs/started/`

Returns story arcs that have been started but not finished by the authenticated user, sorted by most recently read issue.

- **ViewSet**: [`StoryArcsViewSet`](viewsets.md#storyarcsviewset)
- **Action**: `started` (from `StartedActionMixin`)
- **Serializer**: [`StartedStoryArcSerializer`](serializers.md#startedstoryarcserializer)
- **Permissions**: Authenticated users only.
- **Query params**: Standard pagination parameters.
- **Response structure**: Returns arcs with `is_started=True` and `is_finished=False`, sorted by `-max_finished_date`. Each entry contains:
  ```json
  {
    "slug": "dark-knight-returns",
    "display_name": "The Dark Knight Returns",
    "image": "https://.../dkr.jpg",
    "max_finished_date": "2024-06-01T12:00:00Z",
    "finished_count": 2,
    "issues_count": 4
  }
  ```

## Input payloads

All endpoints are read-only; there is no POST/PATCH/DELETE.

## Planned DRF endpoints (status PLAN)

- `GET /api/story-arcs/{slug}/` (detail serializer/detail slug lookup needs work; map lists as `NEEDS WORK`).
- `GET /api/story-arcs/{slug}/technical-info/`
- `GET /api/story-arcs/{slug}/start-watch/`
- `GET /api/story-arcs/{slug}/stop-watch/`
- `GET /api/story-arcs/{slug}/mark-finished/`
- `GET /api/story-arcs/{slug}/died/`
- `GET /api/story-arcs/{slug}/authors/`
- `GET /api/story-arcs/{slug}/characters/`
- `GET /api/story-arcs/{slug}/concepts/`
- `GET /api/story-arcs/{slug}/disbanded/`
- `GET /api/story-arcs/{slug}/first-appearances/`
- `GET /api/story-arcs/{slug}/issues/{issue_slug}/`
- `GET /api/story-arcs/{slug}/locations/`
- `GET /api/story-arcs/{slug}/issues/`
- `GET /api/story-arcs/{slug}/objects/`
- `GET /api/story-arcs/{slug}/teams/`
- `GET /api/story-arcs/{slug}/volumes/`

All these paths are marked `PLAN` (and the detail endpoint as `NEEDS WORK`) in `DRF_MIGRATION_URL_MAP.md`, pending slug-based detail+serializers.