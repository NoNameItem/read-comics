# Frontend Architecture

High-level overview of the Nuxt 4 frontend architecture.

## Summary

- [Technology Stack](#technology-stack) — frameworks and libraries
- [Directory Structure](#directory-structure) — project organization
- [Key Patterns](#key-patterns) — authentication, state management, API integration

## Technology Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| Framework | Nuxt 3 | SSR/SSG Vue.js framework |
| UI Library | Nuxt UI v4 | Component library with dashboard components |
| State Management | Pinia | Reactive stores with persistence |
| HTTP Client | Axios | API requests with interceptors |
| Styling | UnoCSS | Utility-first CSS |
| Color Mode | @nuxtjs/color-mode | Dark/light theme switching |
| Form Validation | Zod | Schema-based validation |
| Icons | Iconify (Lucide) | Icon system |
| Date Utils | date-fns | Date formatting |

## Directory Structure

```
frontend/app/
├── assets/           # Static assets (CSS, images)
│   ├── css/          # Global styles
│   └── images/       # Avatar images
├── components/       # Reusable Vue components
├── composables/      # Composition API utilities
├── layouts/          # Page layouts (default, blank)
├── middleware/       # Route middleware
├── pages/            # File-based routing
├── stores/           # Pinia state stores
├── types/            # TypeScript type definitions
└── utils/            # Helper functions
```

## Key Patterns

### Authentication Flow

1. User submits credentials on `/users/login`
2. [`useUserStore`](stores/user.md) sends POST to `/api/auth/login/`
3. Backend returns JWT tokens + user data
4. Store saves tokens and user profile (persisted to localStorage)
5. [`useAxios`](composables/useAxios.md) interceptor adds `Authorization: Bearer` header to all requests
6. On 401 response, interceptor attempts token refresh via `/api/auth/token/refresh/`
7. If refresh fails, user is logged out and redirected to login

### State Management

Pinia stores with `persist: true` option:
- [`useUserStore`](stores/user.md) — authentication, tokens, user profile
- [`useBreadcrumbsStore`](stores/breadcrumbs.md) — page title and navigation breadcrumbs

### Route Protection

[`auth.global.ts`](middleware/auth.global.md) middleware checks `route.meta.loginRequired`:
- If `true` and user not logged in → redirect to `/users/login?to={currentPath}`
- Additional meta flags: `staffRequired`, `superuserRequired`

### API Integration

[`useAxios`](composables/useAxios.md) composable provides configured Axios instance:
- Base URL: `http://127.0.0.1:8000/api`
- Request interceptor: adds JWT token
- Response interceptor: handles 401 with token refresh

### Layouts

- [`default`](layouts/default.md) — dashboard layout with collapsible sidebar, user menu, breadcrumbs
- [`blank`](layouts/blank.md) — minimal layout for auth pages (login, register)

## Configuration

### app.config.ts

```typescript
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'teal',
      neutral: 'zinc'
    }
  }
})
```

### Runtime Config

- API base URL currently hardcoded in `useAxios.js`
- Future: move to `runtimeConfig` for environment-based configuration