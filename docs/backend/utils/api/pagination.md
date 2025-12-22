# API pagination

`read_comics.utils.api.pagination.Pagination` extends DRF’s `PageNumberPagination` to add a `pages_count` field.

## Response shape

```
{
  "count": 1234,
  "next": "https://.../api/issues/?page=2",
  "previous": null,
  "pages_count": 26,
  "results": [ ... ]
}
```

When pagination is disabled or the page is absent, the viewset simply returns `results` (no wrapper). This pagination class is wired into `REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"]`.
