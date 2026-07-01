# Register Page in `frontend/app/pages/users/register.vue`

User registration page.

## Summary

- [Route](#route) — path and configuration
- [Form](#form) — fields and validation
- [Behavior](#behavior) — submit handling

## Reference

### Route

| Property | Value |
|----------|-------|
| Path | `/users/register` |
| Layout | `blank` |
| Auth Required | No |

### Query Parameters

| Param | Type | Description |
|-------|------|-------------|
| `to` | `string` | Redirect path after successful registration |

## Form

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | `string` | Yes | Desired username |
| `email` | `string` | Yes | Email address |
| `password` | `password` | Yes | Password (min 8 chars) |
| `confirmPassword` | `password` | Yes | Password confirmation |

### Validation Schema (Zod)

```typescript
z.object({
  username: z.string().trim().min(1, 'Username is required'),
  email: z.string().trim().min(1).email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string().min(1, 'Please confirm your password')
}).refine(
  (data) => data.password === data.confirmPassword,
  { message: 'Passwords do not match', path: ['confirmPassword'] }
)
```

## Behavior

### Submit Flow

1. Set `loading = true`, clear `formError`
2. Call `userStore.register(username, email, password)`
3. On error:
   - Status 400: show first error from `username`, `email`, `password1`, or `non_field_errors`
   - Other: show "Network error. Please try again later."
4. On success:
   - Show welcome toast with user name
   - Redirect to `query.to` or `/`

### Error Handling

| Status | Error Source | Display |
|--------|--------------|---------|
| 400 | `username[0]` | Username validation error |
| 400 | `email[0]` | Email validation error |
| 400 | `password1[0]` | Password validation error |
| 400 | `non_field_errors[0]` | General error |
| 400 | fallback | "Registration failed" |
| Other | — | "Network error. Please try again later." |

## UI Components

- `UPageCard` — card container
- `UAuthForm` — Nuxt UI auth form component
- `UAlert` — error display
- `ULink` — link to login page

## Dependencies

- [`useUserStore`](../../stores/user.md) — `register()` method
- `useRoute` — access `query.to`
- `useRouter` — navigation after registration
- `useToast` — success notification

## Related

- [Login page](login.md) — user login
- [`useUserStore.register()`](../../stores/user.md#registerusername-email-password)