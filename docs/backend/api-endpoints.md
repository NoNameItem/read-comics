# DRF API endpoints
A high-level reference for every Django REST Framework endpoint served under `/api/`. The router resides in `config/api_router.py` (uses `ExtendedDefaultRouter` when `DEBUG` is on, otherwise `ExtendedSimpleRouter`), and several custom profile views live in `read_comics/users/api/views.py`.

## Shared behaviors
- **`UniqueOrderingFilter`** ensures every `ordering` query adds `id` as a fallback so pagination stays stable.
- **`CountActionMixin`** exposes `GET /api/<resource>/count/` across all viewsets.
- **`TechnicalInfoActionMixin`** adds `GET /api/<resource>/<slug>/technical-info/`, guarded by `IsSuperuserOrStaff`.
- **`StartedActionMixin`** (volumes and story arcs) exposes `GET /api/<resource>/started/` for authenticated users who have begun but not finished a resource.
- **`OnlyWithIssuesQuerySetMixin`** filters out records without issues unless `?show-all=yes` is passed.
- **`HideFinishedQuerySetMixin`** defaults to `?hide-finished=yes`, hiding records that a user already finished.

## Registered viewsets (`config/api_router.py`)

| Prefix | ViewSet | Source |
| --- | --- | --- |
| `characters` | `CharacterViewSet` | `read_comics/characters/api/viewsets.py` |
| `concepts` | `ConceptViewSet` | `read_comics/concepts/api/viewsets.py` |
| `issues` | `IssueViewSet` | `read_comics/issues/api/viewsets.py` |
| `locations` | `LocationViewSet` | `read_comics/locations/api/viewsets.py` |
| `missing-issues` | `MissingIssueViewSet` | `read_comics/missing_issues/api/viewsets.py` |
| `objects` | `ObjectViewSet` | `read_comics/objects/api/viewsets.py` |
| `people` | `PeopleViewSet` | `read_comics/people/api/viewsets.py` |
| `publishers` | `PublishersViewSet` | `read_comics/publishers/api/viewsets.py` |
| `story-arcs` | `StoryArcsViewSet` | `read_comics/story_arcs/api/viewsets.py` |
| `teams` | `TeamsViewSet` | `read_comics/teams/api/viewsets.py` |
| `volumes` | `VolumesViewSet` | `read_comics/volumes/api/viewsets.py` |

Every router-registered class inherits from `ReadOnlyModelViewSet`, so only `list`/`retrieve` are available plus the mixin-provided `@action` endpoints.

## Documented resources

### Characters (`/api/characters/`)
- `list_only` limits list responses to `slug`, `thumb_url`, `name`, publisher metadata, and `short_description`.
- Supports `ordering=name|issues_count|volumes_count` (default `name`), and `?show-all=yes` to include characters without issues.
- Details use `lookup_field = slug`, so you can fetch `/api/characters/{slug}/`.
- Extra actions:
  - `GET /api/characters/count/`
  - `GET /api/characters/{slug}/technical-info/` (staff+superuser only)

### Concepts (`/api/concepts/`)
- Mirrors characters but the list only exposes `slug`, `thumb_url`, `name`, and `short_description`.
- Same ordering and `show-all` parameters.
- Extra actions:
  - `GET /api/concepts/count/`
  - `GET /api/concepts/{slug}/technical-info/` (staff+superuser)

### Locations (`/api/locations/`)
- Shares the same `list_only` fields as concepts, but technical info uses `ConceptTechnicalInfoSerializer`.
- Supports the same ordering, `show-all`, and slug lookup.
- Extra actions:
  - `GET /api/locations/count/`
  - `GET /api/locations/{slug}/technical-info/` (staff+superuser)

### Issues (`/api/issues/`)
- List responses return metadata from `list_only` plus volume/publisher fields for faster rendering.
- Ordering choices: `cover_date`, `volume__name`, `volume__start_year`, `numerical_number`, `number`.
- `hide-finished=yes` (default) removes fully read issues; authenticated users receive an annotated `finished_flg` to support that filter.
- Context for detail serializers includes `prev`/`next` slugs and the issue’s position inside the current ordered queryset.
- Extra actions:
  - `GET /api/issues/count/`
  - `GET /api/issues/{slug}/technical-info/` (staff+superuser)

### Missing Issues (`/api/missing-issues/`)
- Queryset is restricted to `MissingIssue.objects.filter(skip=False)`.
- Supports list and detail by PK, plus `GET /api/missing-issues/count/`.

### Objects (`/api/objects/`)
- Lists only `slug`, `thumb_url`, `name`, and `short_description`.
- Supports ordering by `name`, `issues_count`, and `volumes_count`.
- Mixins hide items without issues by default (`?show-all=yes` to override).
- Extra action: `GET /api/objects/count/`

### People (`/api/people/`)
- Same list behavior as objects but uses `PeopleListSerializer`.
- Ordering and `show-all` parameters match `ObjectViewSet`.
- Extra action: `GET /api/people/count/`

### Publishers (`/api/publishers/`)
- Similar to people/objects but counts issues through `issues_lookup = "volumes__issues"` and volumes through `volumes_lookup = "volumes"`.
- Extra action: `GET /api/publishers/count/`

### Story Arcs (`/api/story-arcs/`)
- List responses include slug, thumb, name, publisher info, and short description with ordering on `name`, `issues_count`, and `volumes_count`.
- `FinishedQuerySetMixin` annotates `is_started`/`is_finished`, while `HideFinishedQuerySetMixin` hides completed arcs by default.
- `StartedActionMixin` adds `GET /api/story-arcs/started/` (authenticated only).
- Extra action: `GET /api/story-arcs/count/`

### Teams (`/api/teams/`)
- Mirrors the people endpoint with the same ordering and filters.
- Extra action: `GET /api/teams/count/`

### Volumes (`/api/volumes/`)
- `list_only` includes slug, thumb, name, publisher metadata, and short description.
- Ordering fields are `start_year`, `name`, and `issues_count` with default `start_year`.
- Mixins annotate finished/started status and hide finished volumes by default; `?hide-finished=yes` is applied on lists.
- `StartedActionMixin` adds `GET /api/volumes/started/`.
- Extra action: `GET /api/volumes/count/`

## User-focused endpoints

- `api/profile/` (`read_comics/users/api/views.py:ProfileView`) — `GET`, `PATCH`, and `PUT` for profile data using `ProfileSerializer`; requires authentication.
- `api/profile/finished-stats/` (`FinishedIssuesStatsView`) — `GET` returns `{ finished_count, today_finished_count, reading_speed }`.
- `api/profile/change-email/` (`ChangeEmailView`) — `PUT`/`PATCH` updates the primary `EmailAddress` via `ChangeEmailSerializer`; requires authentication.

## Authentication

- `api/auth/` and `api/auth/registration/` wire the standard `dj_rest_auth` login/out, password reset, social, and registration endpoints via `config/urls.py`.

## Adding a new viewset

1. Register it inside `config/api_router.py`.
2. Apply the relevant mixins (`CountActionMixin`, `UniqueOrderingFilter`, etc.) to expose shared behaviors.
3. Update this document (and any specialized `docs/backend/<module>.md`) with the new contract and add a `# Docs: [[...]]` reference at the top of the corresponding Python module.
