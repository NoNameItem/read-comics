# Password Reset Confirm Page Design

**Task:** read_comics-fqr.2
**URL:** `/users/password-reset`
**API:** `POST /api/auth/password/reset/confirm/`

## Query Parameters

Page receives from URL:
- `uid` — user ID
- `token` — reset token
- `email` — email for display (optional)

If `uid` or `token` missing — redirect to `/users/forgot-password`.

## States

### Form State (Initial)

- **Layout:** `blank`
- **Component:** `UPageCard` + `UAuthForm`
- **Title:** "Set new password"
- **Icon:** `i-lucide-key-round`
- **Fields:**
  - `password` — label "New password", type password, placeholder "Enter new password"
  - `confirmPassword` — label "Confirm password", type password, placeholder "Confirm new password"
- **Submit button:** "Save new password"
- **Footer:** none

### Success State

- **Icon:** `i-lucide-check-circle` (color `text-primary`)
- **Title:** "Password changed"
- **Description:** "Your password has been updated. You can now log in with your new password."
- **Button:** "Log in" → `/users/login`

## Validation

### Frontend (Zod)

```typescript
const schema = z.object({
  password: z.string().min(1, 'Password is required'),
  confirmPassword: z.string().min(1, 'Please confirm your password')
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword']
})
```

Password strength validated by backend (Django AUTH_PASSWORD_VALIDATORS).

## Error Handling

| Scenario | HTTP | Behavior |
|----------|------|----------|
| Invalid/expired token | 400 | UAlert: "This password reset link has expired or is invalid. Please request a new one." + "Request new link" button → `/users/forgot-password` |
| Weak password | 400 | Show backend errors under respective fields |
| Network error | — | UAlert: "Network error. Please try again later." |
| Rate limit | 429 | UAlert: server message or "Too many requests. Please try again later." |

## Technical Implementation

### Files

- **Create:** `frontend/app/pages/users/password-reset.vue`
- **Modify:** `read_comics/users/api/serializers.py` — URL in `password_reset_url_generator`

### Component Structure

```
onMounted:
  - Check uid and token in query params
  - If missing — navigateTo('/users/forgot-password')

onSubmit:
  - POST /api/auth/password/reset/confirm/
  - Body: { uid, token, new_password1, new_password2 }
  - Success → show success state
  - Error → show appropriate error
```

### Dependencies

Uses existing:
- `useAxios()` — API requests
- `UPageCard`, `UAuthForm`, `UAlert`, `UButton`, `ULink`, `UIcon` — UI components
