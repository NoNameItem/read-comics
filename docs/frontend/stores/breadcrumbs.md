# Breadcrumbs Store in `frontend/app/stores/breadcrumbs.js`

Page title and navigation breadcrumbs management.

## Summary

- [`useBreadcrumbsStore`](#usebreadcrumbsstore) — main store export
- [State](#state) — reactive state properties
- [Computed](#computed) — derived properties
- [Actions](#actions) — store methods

## Reference

### useBreadcrumbsStore

Pinia store managing page title and breadcrumb navigation.

**Usage:**
```typescript
const breadcrumbs = useBreadcrumbsStore()
breadcrumbs.setBreadcrumbs('Page Title', [
  { label: 'Section', to: '/section' }
])
```

## State

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `pageTitle` | `string` | `''` | Current page title |
| `breadcrumbs` | `array` | `[]` | Breadcrumb items (without home) |
| `loading` | `boolean` | `true` | Loading state flag |

## Computed

### fullBreadcrumbs

Returns complete breadcrumb array with home icon prepended.

- **Type:** `ComputedRef<BreadcrumbItem[]>`
- **Returns:** Array starting with home icon, followed by `breadcrumbs` items

**Structure:**
```typescript
[
  { icon: 'i-lucide-house', to: '/' },
  ...breadcrumbs.map(item => ({ ...item }))
]
```

## Actions

### setBreadcrumbs(newPageTitle, newBreadcrumbs)

Updates page title and breadcrumbs.

- **Parameters:**
  - `newPageTitle`: `string` — new page title
  - `newBreadcrumbs`: `array` — breadcrumb items
- **Side Effects:**
  - Updates `pageTitle` and `breadcrumbs` state
  - Sets document `<title>` via `useHead()` (client-side only)
  - Sets `loading` to `false`

## Breadcrumb Item Format

Each breadcrumb item should follow Nuxt UI's `UBreadcrumb` format:

| Property | Type | Description |
|----------|------|-------------|
| `label` | `string` | Display text |
| `to` | `string` | Navigation path |
| `icon` | `string` | Optional icon class |

## Related

- [`PageWithHeader`](../components/PageWithHeader.md) — component displaying breadcrumbs