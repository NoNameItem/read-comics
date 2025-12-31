# Pinia Stores

State management using Pinia with persistence.

## Documentation

- [user.md](user.md) — Authentication, tokens, and user profile
- [breadcrumbs.md](breadcrumbs.md) — Page title and navigation breadcrumbs

## Overview

All stores use Pinia's Composition API syntax with `defineStore()` and the `persist: true` option for localStorage persistence.

### Store Pattern

```typescript
export const useMyStore = defineStore('storeName', () => {
  // State
  const myState = ref(null)

  // Computed
  const myComputed = computed(() => /* ... */)

  // Actions
  const myAction = async () => { /* ... */ }

  return { myState, myComputed, myAction }
}, { persist: true })
```

### Persistence

Stores with `persist: true` automatically:
- Save state to localStorage on changes
- Restore state on page reload
- Provide `$hydrate()` and `$persist()` methods for manual control