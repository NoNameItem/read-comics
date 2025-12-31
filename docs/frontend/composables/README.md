# Composables

Vue Composition API utilities.

## Documentation

- [useAxios.md](useAxios.md) — Axios HTTP client with JWT interceptors

## Overview

Composables are reusable functions that encapsulate reactive logic using Vue's Composition API. They follow the `use*` naming convention and can be auto-imported by Nuxt.

### Composable Pattern

```typescript
export function useMyComposable() {
  // Reactive state
  const data = ref(null)

  // Methods
  const fetchData = async () => { /* ... */ }

  return { data, fetchData }
}
```