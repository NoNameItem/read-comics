# Forgot Password Page in `frontend/app/pages/users/forgot-password.vue`

Password reset request page.

## Summary

- [Route](#route) — path and configuration
- [States](#states) — form and success states
- [Behavior](#behavior) — submit and resend handling

## Reference

### Route

| Property | Value |
|----------|-------|
| Path | `/users/forgot-password` |
| Layout | `blank` |
| Auth Required | No |

## States

### Form State

Initial state with email input form.

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | `email` | Yes | User email address |

#### Validation Schema (Zod)

```typescript
z.object({
  email: z.string().trim().min(1, 'Email is required').email('Invalid email address')
})
```

### Success State

Displayed after successful form submission. Shows confirmation message and resend button.

#### Elements

| Element | Description |
|---------|-------------|
| Icon | `i-lucide-mail-check` |
| Title | "Check your email" |
| Message | "We sent a password reset link to **{email}**" |
| Resend button | Disabled for 60s after send, shows countdown |
| Back link | Returns to `/users/login` |

## Behavior

### Submit Flow

1. Set `loading = true`, clear `formError`
2. POST to `/api/auth/password/reset/` with `{ email }`
3. On success or 400 (security: don't reveal if email exists):
   - Store email, switch to success state
   - Start 60-second resend cooldown
4. On 429: show rate limit error
5. On other errors: show "Network error. Please try again later."

### Resend Flow

1. Set `loading = true`, clear `formError`
2. POST to `/api/auth/password/reset/` with stored email
3. On success or 400: restart 60-second cooldown
4. On 429: show rate limit error
5. On other errors: show "Network error. Please try again later."

### Error Handling

| Status | Display |
|--------|---------|
| 400 | Show success (security) |
| 429 | Server message or "Too many requests. Please try again later." |
| Other | "Network error. Please try again later." |

## UI Components

- `UPageCard` — card container
- `UAuthForm` — form state
- `UButton` — resend button
- `UAlert` — error display
- `UIcon` — success state icon
- `ULink` — navigation links

## Dependencies

- `useAxios` — API calls
- `onUnmounted` — cleanup cooldown interval

## Related

- [Login page](login.md) — links to this page
