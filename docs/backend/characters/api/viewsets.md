# Viewset in `characters/api/viewsets.py`

## Summary

- [`CharacterViewSet`](#characterviewset) — read-only DRF viewset for [`Character`](../models.md#character) resources at `/api/characters/`; provides list/detail operations with filtering, ordering, and custom actions (`count`, `technical-info`).

## Reference

### `CharacterViewSet`

- Django REST Framework read-only viewset combining multiple mixins for robust character querying, filtering, and metadata aggregation.
- Inherits from `ReadOnlyModelViewSet` plus custom mixins for detail serializer switching, technical info exposure, and queryset enrichment.
- Powers `/api/characters/` REST API endpoint.

#### Base classes & mixins

- `DetailSerializerMixin` — switches serializer class between list and detail responses; uses `CharactersListSerializer` for list and `CharacterDetailSerializer` for retrieve.
- `TechnicalInfoActionMixin` — adds `/technical-info/` custom action (restricted to superuser/staff) exposing administrative metadata.
- `CountActionMixin` — adds `/count/` custom action returning total record count after filtering.
- `OnlyWithIssuesQuerySetMixin` — filters queryset to characters with matched issues unless `?show-all=yes` query parameter is provided.
- `IssuesCountQuerySetMixin` — annotates queryset with `issues_count` field for efficient list serialization.
- `VolumesCountQuerySetMixin` — annotates queryset with `volumes_count` field for efficient list serialization.
- `ListOnlyQuerySetMixin` — restricts field retrieval in list responses to minimize database load.

#### Configuration attributes

- `list_only` (list[str]): Fields to retrieve in list queries for optimization; includes `slug`, `thumb_url`, `name`, publisher metadata, and `short_description`. Other fields are deferred.
- `serializer_class = CharactersListSerializer`: Default serializer for list/search responses.
- `serializer_detail_class = CharacterDetailSerializer`: Serializer for detail/retrieve responses.
- `serializer_tech_info_class = CharacterTechnicalInfoSerializer`: Serializer for technical-info action responses.
- `filter_backends = [UniqueOrderingFilter]`: Ordering filter that appends `id` to ensure stable pagination.
- `ordering_fields = ["name", "issues_count", "volumes_count"]`: Allowed ordering directions.
- `ordering = ["name"]`: Default ordering (alphabetical by name).
- `lookup_field = "slug"`: Lookup field for detail views (characters are identified by slug, not PK).
- `lookup_url_kwarg = "slug"`: URL kwarg name matching `lookup_field`.

#### Properties

- `queryset` (property)
  - **Getter**: Returns queryset of characters that have been matched to ComicVine data, with publisher relation pre-fetched.
  - Returns: `Character.objects.was_matched().select_related("publisher")`
  - Purpose: Filters out unmatched characters and optimizes queries with `select_related`.
  - **Setter**: Disabled (returns without action) to prevent assignment of custom querysets.

#### Inherited actions

- `list` (`GET /api/characters/`) — returns paginated list of characters with compact fields from `CharactersListSerializer`. Supports:
  - `ordering=name|issues_count|volumes_count` query parameter (default: `name`)
  - `?show-all=yes` to include characters without issues
  - Standard DRF pagination query parameters (`page`, `page_size`)

- `retrieve` (`GET /api/characters/{slug}/`) — returns character detail via `CharacterDetailSerializer`. Path parameter `slug` must match a character's slug field.

- `count` (`GET /api/characters/count/`) — custom action from `CountActionMixin`; returns `{"count": <int>}` after applying active filters.

- `technical_info` (`GET /api/characters/{slug}/technical-info/`) — custom action from `TechnicalInfoActionMixin` (superuser/staff only); returns administrative metadata via `CharacterTechnicalInfoSerializer`.

## Filter & ordering behavior

- **`UniqueOrderingFilter`** ensures every ordering always includes `id` as a fallback, preventing pagination ambiguity when multiple records share the same `name`/`issues_count`/`volumes_count`.
- **Default ordering** is by character name ascending; users can override via `?ordering=<field>`.
- **`OnlyWithIssuesQuerySetMixin`** filters to `was_matched()` characters unless `?show-all=yes` is passed, reducing noise for end users while allowing administrators to see all records.

## API endpoint structure

```
GET /api/characters/                          → list action
GET /api/characters/{slug}/                   → retrieve action
GET /api/characters/count/                    → count action
GET /api/characters/{slug}/technical-info/    → technical_info action
```

## Example requests

### List characters with default ordering

```
GET /api/characters/
Content-Type: application/json
```

Response:
```json
{
  "count": 150,
  "next": "http://example.com/api/characters/?page=2",
  "previous": null,
  "results": [
    {
      "slug": "batman",
      "image": "https://cdn.example.com/batman.jpg",
      "publisher": {"name": "DC", "slug": "dc", "image": "https://..."},
      "name": "Batman",
      "short_description": "The Dark Knight of Gotham.",
      "issues_count": 2500,
      "volumes_count": 80
    }
  ]
}
```

### Retrieve character detail

```
GET /api/characters/spider-man/
Content-Type: application/json
```

Response:
```json
{
  "slug": "spider-man",
  "name": "Spider-Man",
  "real_name": "Peter Parker",
  "image": "https://cdn.example.com/spiderman_full.jpg",
  "square_image": "https://cdn.example.com/spiderman_square.jpg",
  "publisher": {"name": "Marvel", "slug": "marvel", "image": "https://..."},
  "aliases": ["Spidey", "Web-Slinger", "Friendly Neighborhood Spider-Man"],
  "birth": "1962-06-01",
  "gender": "Male",
  "powers": ["Super Strength", "Web Shooting", "Wall Crawling"],
  "first_issue_name": "Amazing Fantasy #15",
  "first_issue_slug": "amazing-fantasy-15",
  "comicvine_url": "https://comicvine.gamespot.com/spider-man/4005-1234/",
  "short_description": "Your friendly neighborhood Spider-Man.",
  "description": "<p>Peter Parker gained spider powers...</p>",
  "download_link": "http://example.com/download/spider-man.zip",
  "download_size": "256 MB"
}
```

### Get character count

```
GET /api/characters/count/
Content-Type: application/json
```

Response:
```json
{
  "count": 150
}
```

### Get character technical info (staff only)

```
GET /api/characters/batman/technical-info/
Authorization: Bearer <token>
Content-Type: application/json
```

Response:
```json
{
  "id": 1,
  "comicvine_id": 12345,
  "comicvine_status": "Matched",
  "comicvine_last_match": "2025-12-22T12:00:00Z",
  "created_dt": "2020-01-01T00:00:00Z",
  "modified_dt": "2025-12-22T12:00:00Z"
}
```

## Related documentation

- [`Character` model documentation](../models.md)
- [Character serializers documentation](serializers.md)
- [Character API endpoints reference](endpoints.md)
- [DRF API endpoints overview](../../api-endpoints.md)