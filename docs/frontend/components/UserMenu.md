# UserMenu in `frontend/app/components/UserMenu.vue`

User dropdown menu displayed in sidebar footer.

## Summary

- [Props](#props) — component properties
- [Behavior](#behavior) — logged in vs logged out states
- [Menu Items](#menu-items) — dropdown menu structure

## Reference

### UserMenu

Displays user avatar with dropdown menu when logged in, or login button when logged out.

**Location:** Sidebar footer in [`default` layout](../layouts/default.md)

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `collapsed` | `boolean` | `false` | Sidebar collapsed state |

## Behavior

### Logged In State

Displays `UDropdownMenu` with:
- User avatar thumbnail
- User display name (unless collapsed)
- Chevron icon (unless collapsed)

**Menu sections:**
1. User label with avatar
2. Profile link
3. Log out action

### Logged Out State

Displays `UButton` linking to login page:
- "Log in" label (unless collapsed)
- Login icon
- Preserves current path in `to` query param

### Logout Flow

1. Checks if current route requires auth (`loginRequired`, `staffRequired`, `superuserRequired`)
2. Calls `userStore.logout()`
3. If route requires auth — redirects to `/users/login?to={currentPath}`
4. Otherwise — stays on current page

## Menu Items

```typescript
[
  [{ type: 'label', label: userName, avatar: userAvatar }],
  [{ label: 'Profile', icon: 'i-lucide-user' }],
  [{ label: 'Log out', icon: 'i-lucide-log-out', onSelect: handleLogout }]
]
```

## Dependencies

- [`useUserStore`](../stores/user.md) — user state and logout method
- `useRoute` — current route for redirect logic

## Related

- [`default` layout](../layouts/default.md) — uses UserMenu in footer