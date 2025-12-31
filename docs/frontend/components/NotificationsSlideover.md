# NotificationsSlideover in `frontend/app/components/NotificationsSlideover.vue`

Notifications panel component (placeholder from Nuxt UI template).

## Summary

- [Status](#status) — implementation status
- [Structure](#structure) — component layout
- [Dependencies](#dependencies) — required composables

## Status

**Not implemented** — This is a placeholder component from the Nuxt UI dashboard template. It requires:
- `useDashboard()` composable (not yet created)
- `/api/notifications` endpoint (not yet implemented)
- `Notification` type definition

## Structure

Displays notifications in a slideover panel:
- Each notification shows sender avatar, name, body, and relative time
- Links to `/inbox?id={notification.id}`
- Unread indicator via `UChip`

## Dependencies

| Dependency | Status | Description |
|------------|--------|-------------|
| `useDashboard()` | Missing | Controls `isNotificationsSlideoverOpen` |
| `/api/notifications` | Missing | Backend endpoint for notifications |
| `Notification` type | Removed | Was placeholder, needs real definition |

## Future Implementation

To implement notifications:
1. Create `useDashboard` composable with `isNotificationsSlideoverOpen` ref
2. Add notifications API endpoint in Django backend
3. Define `Notification` interface matching backend response
4. Update component to use real data