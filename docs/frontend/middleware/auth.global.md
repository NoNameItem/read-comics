# Auth Middleware in `frontend/app/middleware/auth.global.ts`

Global authentication guard middleware.

## Summary

- [Behavior](#behavior) — route protection logic
- [Route Meta](#route-meta) — protection flags

## Reference

### Behavior

Runs on every navigation to check authentication requirements.

**Flow:**
1. Get user store via `useUserStore()`
2. Check if route has `meta.loginRequired`
3. If required and user not logged in:
   - Redirect to `/users/login`
   - Preserve original path in `to` query param

### Route Protection

```typescript
if (to.meta?.loginRequired && !user.loggedIn) {
  return navigateTo({
    path: '/users/login',
    query: { to: to.fullPath }
  })
}
```

## Route Meta

Set in page `definePageMeta()`:

| Flag | Type | Description |
|------|------|-------------|
| `loginRequired` | `boolean` | Requires authenticated user |
| `staffRequired` | `boolean` | Requires staff privileges (checked in [`useAxios`](../composables/useAxios.md)) |
| `superuserRequired` | `boolean` | Requires superuser privileges (checked in [`useAxios`](../composables/useAxios.md)) |

### Example

```typescript
definePageMeta({
  loginRequired: true
})
```

## Dependencies

- [`useUserStore`](../stores/user.md) — provides `loggedIn` computed

## Related

- [`useAxios`](../composables/useAxios.md) — checks staff/superuser on 401
- [Routes](../routes.md) — route meta configuration