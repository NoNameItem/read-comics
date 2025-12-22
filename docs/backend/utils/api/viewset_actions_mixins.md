# Viewset action mixins

## Shared actions

Many viewsets reuse these mixins to expose consistent helper endpoints.

### `CountActionMixin`
- Provides `GET /api/<resource>/count/`.
- Returns `{"count": queryset.count()}` for the currently filtered queryset.

### `TechnicalInfoActionMixin`
- Adds `GET /api/<resource>/<slug>/technical-info/`.
- Requires `serializer_tech_info_class` and `IsSuperuserOrStaff`.
- Serializes the instance using the supplied serializer class to surface ComicVine/internal metadata.

### `StartedActionMixin`
- Adds `GET /api/<resource>/started/` (volumes, story arcs).
- Requires user authentication.
- Filters resources with `is_started=True` and `is_finished=False`, orders by `-max_finished_date`, and returns paginated data through `started_serializer`.
