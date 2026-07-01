# Frontend Routes

Overview of all application routes defined in `frontend/app/pages/`.

## Summary

- [Public Routes](#public-routes) — accessible without authentication
- [Auth Routes](#auth-routes) — login, registration
- [Route Meta](#route-meta) — protection flags

## Routes Table

| Path | Page | Layout | Auth Required | Description |
|------|------|--------|---------------|-------------|
| `/` | [index.vue](pages/index.md) | default | No | Home page |
| `/users/login` | [login.vue](pages/users/login.md) | blank | No | User login form |
| `/users/register` | [register.vue](pages/users/register.md) | blank | No | User registration form |

## Public Routes

### `/` — Home

- **Page:** [`pages/index.vue`](pages/index.md)
- **Layout:** [`default`](layouts/default.md)
- **Description:** Application home page with dashboard layout

## Auth Routes

### `/users/login` — Login

- **Page:** [`pages/users/login.vue`](pages/users/login.md)
- **Layout:** [`blank`](layouts/blank.md)
- **Query params:**
  - `to` — redirect path after successful login
- **Description:** Login form with Zod validation, error handling, redirect support

### `/users/register` — Registration

- **Page:** [`pages/users/register.vue`](pages/users/register.md)
- **Layout:** [`blank`](layouts/blank.md)
- **Query params:**
  - `to` — redirect path after successful registration
- **Description:** Registration form with email, username, password fields

## Route Meta

Routes can define meta flags in `definePageMeta()`:

| Flag | Type | Description |
|------|------|-------------|
| `loginRequired` | `boolean` | Requires authenticated user |
| `staffRequired` | `boolean` | Requires staff privileges |
| `superuserRequired` | `boolean` | Requires superuser privileges |
| `layout` | `string` | Layout to use (`default`, `blank`) |

### Example

```typescript
definePageMeta({
  layout: 'blank',
  loginRequired: true
})
```

## Middleware

All routes pass through [`auth.global.ts`](middleware/auth.global.md) middleware which:
1. Checks `route.meta.loginRequired`
2. Redirects to `/users/login?to={path}` if not authenticated