# Frontend (Nuxt 3)

The client is built with Nuxt 3 and runs independently from Django.

## Overview

- [Architecture](architecture.md) — technology stack, directory structure, key patterns
- [Routes](routes.md) — application routes and navigation

## Development

- [Development and local setup](development.md)
- [Build, preview, and linting](build.md)

## Modules

### State Management
- [Stores](stores/README.md) — Pinia stores
  - [user.md](stores/user.md) — authentication and user profile
  - [breadcrumbs.md](stores/breadcrumbs.md) — page title and navigation

### Composables
- [Composables](composables/README.md) — Composition API utilities
  - [useAxios.md](composables/useAxios.md) — HTTP client with JWT interceptors

### Components
- [Components](components/README.md) — reusable Vue components
  - [UserMenu.md](components/UserMenu.md) — user dropdown in sidebar
  - [PageWithHeader.md](components/PageWithHeader.md) — dashboard panel wrapper
  - [NotificationsSlideover.md](components/NotificationsSlideover.md) — notifications panel (placeholder)

### Layouts
- [Layouts](layouts/README.md) — page layouts
  - [default.md](layouts/default.md) — dashboard with sidebar
  - [blank.md](layouts/blank.md) — minimal for auth pages

### Middleware
- [Middleware](middleware/README.md) — route middleware
  - [auth.global.md](middleware/auth.global.md) — authentication guard

### Pages
- [Pages](pages/README.md) — application pages
  - [index.md](pages/index.md) — home page
  - [users/login.md](pages/users/login.md) — login page
  - [users/register.md](pages/users/register.md) — registration page

### Types & Utils
- [Types](types/README.md) — TypeScript definitions
  - [index.md](types/index.md) — project types
- [Utils](utils/README.md) — helper functions
  - [index.md](utils/index.md) — random utilities

## Directory Structure

```
frontend/app/
├── assets/           # Static assets (CSS, images)
├── components/       # Reusable Vue components
├── composables/      # Composition API utilities
├── layouts/          # Page layouts
├── middleware/       # Route middleware
├── pages/            # File-based routing
├── stores/           # Pinia state stores
├── types/            # TypeScript definitions
└── utils/            # Helper functions
```