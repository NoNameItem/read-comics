# Password Reset Request Page Design

**Task:** read_comics-fqr.1
**URL:** `/users/forgot-password`
**API:** `POST /api/auth/password/reset/`

## States

### Initial State (Form)

- **Title:** "Forgot your password?"
- **Icon:** `i-lucide-key-round`
- **Field:** email (required, email format validation)
- **Submit button:** "Send reset link"
- **Footer link:** "Remember your password? Log in" → `/users/login`

### Success State

- **Icon:** `i-lucide-mail-check`
- **Title:** "Check your email"
- **Description:** "We sent a password reset link to **{email}**"
- **Resend button:** "Resend email"
  - Disabled for 60 seconds after send
  - Shows countdown: "Resend in 45s"
  - Client-side timer only (resets on page refresh)
- **Footer link:** "Back to login" → `/users/login`

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Email not found | Show success state (security: don't reveal account existence) |
| Network error | Show `UAlert` with "Network error. Please try again later." |
| Rate limited (429) | Show `UAlert` with server message or "Too many requests" |

## Technical Details

- Layout: `blank`
- Components: `UPageCard`, `UAuthForm` (initial), custom success view
- Validation: Zod schema with email format
- Update login.vue "Forgot password?" link to point to `/users/forgot-password`
