# Default Layout in `frontend/app/layouts/default.vue`

Dashboard layout with collapsible sidebar.

## Summary

- [Structure](#structure) — layout organization
- [Sidebar](#sidebar) — navigation and user menu
- [Menu Items](#menu-items) — navigation configuration

## Reference

### Structure

```
UDashboardGroup
├── UDashboardSidebar
│   ├── header: Brand navigation (logo + "Read Comics")
│   ├── default: Search button + Navigation menu
│   └── footer: UserMenu component
└── <slot /> (page content)
```

## Sidebar

### Configuration

| Property | Value | Description |
|----------|-------|-------------|
| `id` | `"default"` | Sidebar identifier |
| `collapsible` | `true` | Can be collapsed |
| `resizable` | `true` | Can be resized |

### Header

Brand navigation with:
- Logo image (`/images/logo.png`)
- "Read Comics" label
- Link to home (`/`)

### Default Section

- `UDashboardSearchButton` — search trigger
- `UNavigationMenu` — main navigation items

### Footer

- [`UserMenu`](../components/UserMenu.md) component

## Menu Items

Currently configured navigation:

| Label | Icon | Path |
|-------|------|------|
| Home | `i-lucide-house` | `/` |

### Menu Item Structure

```typescript
{
  label: 'Home',
  icon: 'i-lucide-house',
  to: '/',
  onSelect: () => { open.value = false }
}
```

## State

| State | Type | Description |
|-------|------|-------------|
| `open` | `Ref<boolean>` | Sidebar open state (mobile) |

## Related

- [`UserMenu`](../components/UserMenu.md) — footer component
- [`blank` layout](blank.md) — alternative minimal layout