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

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: 'http://127.0.0.1:8000/api'
    }
  }
})
```

Environment variables:
- `.env.development`: `NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api`
- `.env.production`: `NUXT_PUBLIC_API_BASE=https://readcomics.net/api`

## Data Fetching (Pinia Colada)

### Query Pattern

Keys Factory + defineQuery hybrid:

```typescript
// composables/api/characters.ts

export const characterKeys = {
  all: ['characters'] as const,
  lists: () => [...characterKeys.all, 'list'] as const,
  list: (params: object) => [...characterKeys.lists(), params] as const,
  details: () => [...characterKeys.all, 'detail'] as const,
  detail: (slug: string) => [...characterKeys.details(), slug] as const,
}

export const useCharactersList = defineQuery(() => {
  const route = useRoute()
  const axios = useAxios()

  return {
    key: () => characterKeys.list(route.query),
    query: async () => {
      const { data } = await axios.get('/characters/', { params: route.query })
      return data
    },
    staleTime: 5 * 60 * 1000  // 5 min
  }
})
```

### Caching Strategy

| Data Type | staleTime | gcTime |
|-----------|-----------|--------|
| Entity lists | 5 min | 30 min |
| Entity details | 5 min | 30 min |
| Profile / reading progress | 1 min | 30 min |

### Mutations

Pessimistic updates with cache invalidation:

```typescript
export const useMarkIssueRead = defineMutation(() => {
  const axios = useAxios()
  const cache = useQueryCache()

  return {
    mutation: async (issueSlug: string) => {
      await axios.post(`/issues/${issueSlug}/mark-read/`)
    },
    onSuccess: (_data, issueSlug) => {
      // Invalidate all affected caches
      cache.invalidateQueries({ key: issueKeys.all })
      cache.invalidateQueries({ key: volumeKeys.all })
      cache.invalidateQueries({ key: storyArcKeys.all })
      cache.invalidateQueries({ key: profileKeys.all })
      // ... all entities with reading progress
    }
  }
})
```

## Forms and Validation

### Schema (Zod)

Schemas defined inline in components (1 component = 1 schema).

### Server Error Handling

```typescript
// composables/useFormErrors.ts
export function useFormErrors(formRef: Ref<FormInstance | null>) {
  async function handleSubmit<T>(submitFn: () => Promise<T>): Promise<T | undefined> {
    try {
      return await submitFn()
    } catch (error) {
      if (isAxiosError(error) && error.response?.status === 400) {
        const errors = Object.entries(error.response.data).map(
          ([path, messages]) => ({
            path,
            message: Array.isArray(messages) ? messages[0] : messages
          })
        )
        formRef.value?.setErrors(errors)
        return undefined
      }
      throw error
    }
  }

  return { handleSubmit }
}
```

## TypeScript Types

Generated from OpenAPI schema:

```bash
npm run generate:types  # openapi-ts --input ../schema.yaml --output app/types/api
```

Structure:
```
types/
├── api/           # Generated
│   ├── models/
│   │   ├── Character.ts
│   │   ├── Volume.ts
│   │   └── ...
│   └── index.ts
└── index.d.ts     # Manual types
```

## SSR/SSG Strategy

| Pages | Mode | Reason |
|-------|------|--------|
| Entity lists/details | SSR | SEO |
| Search | SSR | SEO |
| Auth, Profile | CSR | Private |
| Missing issues (admin) | CSR | Staff only |

```typescript
// nuxt.config.ts
routeRules: {
  '/users/**': { ssr: false },
  '/missing-issues/**': { ssr: false },
}
```

## Error Handling

| Error | Handler |
|-------|---------|
| 401 | axios interceptor → redirect to login |
| 403 | axios interceptor → toast |
| 400 | useFormErrors → inline form errors |
| 404/500 | error.vue (UError component) |

## SEO

```vue
<script setup>
useSeoMeta({
  title: () => entity.value?.name,
  description: () => entity.value?.short_description,
  ogImage: () => entity.value?.image
})
</script>
```