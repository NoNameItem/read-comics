# PageWithHeader in `frontend/app/components/PageWithHeader.vue`

Dashboard panel wrapper with navbar and breadcrumbs.

## Summary

- [Structure](#structure) — component layout
- [Slots](#slots) — content slots
- [Features](#features) — navbar elements

## Reference

### PageWithHeader

Wraps page content in `UDashboardPanel` with navigation bar.

**Usage:**
```vue
<PageWithHeader>
  <YourPageContent />
</PageWithHeader>
```

## Structure

```
UDashboardPanel
├── header (UDashboardNavbar)
│   ├── leading: UDashboardSidebarCollapse
│   ├── title: pageTitle from breadcrumbs store
│   ├── trailing: UBreadcrumb
│   └── right: UColorModeSelect
└── body
    └── <slot />
```

## Slots

| Slot | Description |
|------|-------------|
| `default` | Page content rendered in body section |

## Features

### Navbar Elements

| Position | Component | Description |
|----------|-----------|-------------|
| Leading | `UDashboardSidebarCollapse` | Sidebar toggle button |
| Title | `pageTitle` | From [`useBreadcrumbsStore`](../stores/breadcrumbs.md) |
| Trailing | `UBreadcrumb` | Full breadcrumbs with home icon |
| Right | `UColorModeSelect` | Dark/light mode toggle |

### Styling

- Title: `text-primary text-lg`
- Breadcrumbs: left border with primary color, padding-left

## Dependencies

- [`useBreadcrumbsStore`](../stores/breadcrumbs.md) — page title and breadcrumbs

## Related

- [`default` layout](../layouts/default.md) — contains PageWithHeader usage