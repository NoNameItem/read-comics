# Home Page in `frontend/app/pages/index.vue`

Application home page.

## Summary

- [Route](#route) — path and layout
- [Features](#features) — page functionality

## Reference

### Route

| Property | Value |
|----------|-------|
| Path | `/` |
| Layout | `default` |
| Auth Required | No |

### Features

- Sets page title via `useServerSeoMeta({ title: 'Read Comics' })`
- Sets breadcrumbs to empty (home page)
- Wrapped in [`PageWithHeader`](../components/PageWithHeader.md) component

### Setup

```typescript
const breadcrumb = useBreadcrumbsStore()
useServerSeoMeta({ title: 'Read Comics' })
breadcrumb.setBreadcrumbs('Read Comics', [])
```

## Dependencies

- [`useBreadcrumbsStore`](../stores/breadcrumbs.md) — page title and breadcrumbs
- [`PageWithHeader`](../components/PageWithHeader.md) — page wrapper

## Related

- [Routes](../routes.md) — all application routes