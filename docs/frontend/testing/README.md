# Frontend Testing

Overview of the Nuxt frontend testing strategy and patterns.

## Testing Stack

| Layer | Tool | Priority |
|-------|------|----------|
| Composables | Vitest | High |
| Components | Vitest + Vue Test Utils | Medium |
| E2E | Playwright | Low (later) |

## Directory Structure

```
frontend/
├── app/
│   ├── composables/
│   │   ├── useFormErrors.ts
│   │   └── useFormErrors.test.ts    # Co-located tests
│   └── components/
│       └── ...
└── tests/                            # E2E tests (future)
    └── e2e/
```

## Composable Tests

Priority: **High** — composables contain business logic.

### Example: useFormErrors

```typescript
// composables/useFormErrors.test.ts
import { describe, it, expect, vi } from 'vitest'
import { ref } from 'vue'
import { useFormErrors } from './useFormErrors'

describe('useFormErrors', () => {
  it('sets form errors on 400 response', async () => {
    const setErrors = vi.fn()
    const formRef = ref({ setErrors })

    const { handleSubmit } = useFormErrors(formRef)

    const error = {
      isAxiosError: true,
      response: {
        status: 400,
        data: { email: ['Already exists'] }
      }
    }

    await handleSubmit(() => Promise.reject(error))

    expect(setErrors).toHaveBeenCalledWith([
      { path: 'email', message: 'Already exists' }
    ])
  })

  it('rethrows non-400 errors', async () => {
    const formRef = ref({ setErrors: vi.fn() })
    const { handleSubmit } = useFormErrors(formRef)

    const error = new Error('Network error')

    await expect(handleSubmit(() => Promise.reject(error))).rejects.toThrow('Network error')
  })

  it('returns result on success', async () => {
    const formRef = ref({ setErrors: vi.fn() })
    const { handleSubmit } = useFormErrors(formRef)

    const result = await handleSubmit(() => Promise.resolve({ id: 1 }))

    expect(result).toEqual({ id: 1 })
  })
})
```

### Example: API Composable

```typescript
// composables/api/characters.test.ts
import { describe, it, expect, vi } from 'vitest'
import { useCharactersList } from './characters'

// Mock dependencies
vi.mock('../useAxios', () => ({
  useAxios: () => ({
    get: vi.fn().mockResolvedValue({
      data: { count: 1, results: [{ slug: 'batman', name: 'Batman' }] }
    })
  })
}))

vi.mock('vue-router', () => ({
  useRoute: () => ({ query: { page: 1 } })
}))

describe('useCharactersList', () => {
  it('returns query with correct key', () => {
    const query = useCharactersList()

    expect(query.key()).toEqual(['characters', 'list', { page: 1 }])
  })
})
```

## Component Tests

Priority: **Medium** — focus on complex components with logic.

### What to Test

- Props rendering
- Event emissions
- Slot content
- Conditional rendering
- User interactions

### Example

```typescript
// components/entity/EntityCard.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import EntityCard from './EntityCard.vue'

describe('EntityCard', () => {
  it('renders name and description', () => {
    const wrapper = mount(EntityCard, {
      props: {
        slug: 'batman',
        name: 'Batman',
        description: 'Dark Knight',
        image: '/batman.jpg',
        tags: ['100 issues']
      }
    })

    expect(wrapper.text()).toContain('Batman')
    expect(wrapper.text()).toContain('Dark Knight')
  })

  it('shows finished badge when isFinished is true', () => {
    const wrapper = mount(EntityCard, {
      props: {
        slug: 'batman',
        name: 'Batman',
        image: '/batman.jpg',
        isFinished: true
      }
    })

    expect(wrapper.find('[data-testid="finished-badge"]').exists()).toBe(true)
  })
})
```

## E2E Tests (Future)

Priority: **Low** — implement after core features are stable.

### Planned Coverage

- Authentication flow (login, logout, registration)
- Entity list navigation and pagination
- Entity detail page tabs
- Mark as read functionality
- Search

### Tool: Playwright

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test('user can login', async ({ page }) => {
  await page.goto('/users/login')
  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'password123')
  await page.click('button[type="submit"]')

  await expect(page).toHaveURL('/')
  await expect(page.locator('[data-testid="user-menu"]')).toBeVisible()
})
```

## Running Tests

```bash
# Unit tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage

# E2E (future)
npm run test:e2e
```

## Best Practices

1. **Co-locate tests** — `useFormErrors.test.ts` next to `useFormErrors.ts`
2. **Mock external dependencies** — axios, router, stores
3. **Test behavior, not implementation** — focus on inputs/outputs
4. **Use descriptive names** — `it('sets form errors on 400 response')`
5. **Keep tests fast** — avoid unnecessary setup
