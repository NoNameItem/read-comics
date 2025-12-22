# API filters

## `UniqueOrderingFilter`

- Subclasses `rest_framework.filters.OrderingFilter`.
- Ensures every ordering list gets `id` appended so pagination produces stable results even when clients request identical values for their sort fields.
- Used throughout DRF viewsets (characters, issues, etc.) via `filter_backends = [UniqueOrderingFilter]`.

### Example

```
GET /api/characters/?ordering=-name
```

Internally the filter turns the orderings into `["-name", "id"]`, guaranteeing consistent cursor positions and preventing duplicates between pages.
