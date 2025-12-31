# Login Page in `frontend/app/pages/users/login.vue`

User authentication page.

## Summary

- [Route](#route) — path and configuration
- [Form](#form) — fields and validation
- [Behavior](#behavior) — submit handling

## Reference

### Route

| Property | Value |
|----------|-------|
| Path | `/users/login` |
| Layout | `blank` |
| Auth Required | No |

### Query Parameters

| Param | Type | Description |
|-------|------|-------------|
| `to` | `string` | Redirect path after successful login |

## Form

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `login` | `string` | Yes | Username or email |
| `password` | `password` | Yes | User password |

### Validation Schema (Zod)

```typescript
z.object({
  login: z.string().trim().min(1, 'Login is required'),
  password: z.string().trim().min(1, 'Password is required')
})
```

## Behavior

### Submit Flow

1. Set `loading = true`, clear `formError`
2. Call `userStore.login(login, password)`
3. On error:
   - Status 400: show `non_field_errors[0]` or "Invalid credentials"
   - Other: show "Network error. Please try again later."
4. On success:
   - Show welcome toast with user name
   - Redirect to `query.to` or `/`

### Error Handling

| Status | Error Source | Display |
|--------|--------------|---------|
| 400 | `non_field_errors[0]` | First validation error |
| 400 | fallback | "Invalid credentials" |
| Other | — | "Network error. Please try again later." |

## UI Components

- `UPageCard` — card container
- `UAuthForm` — Nuxt UI auth form component
- `UAlert` — error display
- `ULink` — link to registration page

## Dependencies

- [`useUserStore`](../../stores/user.md) — `login()` method
- `useRoute` — access `query.to`
- `useRouter` — navigation after login
- `useToast` — success notification

## Related

- [Register page](register.md) — user registration
- [`useUserStore.login()`](../../stores/user.md#loginusername-password)