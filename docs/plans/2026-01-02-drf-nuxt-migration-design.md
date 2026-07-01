# DRF + Nuxt Migration Design

Постраничный план миграции с Django views на DRF API + Nuxt 4 (+ Nuxt UI).

**Стратегия:**
- Flow: Auth + Profile → Home → Lists → Details → Search → Admin
- Backend работа: по ходу дела (встретили блокер → фиксим)
- Релиз: один большой (Django остаётся до полной готовности)

**Оценки сложности:**
- **S** — простая страница/компонент, API готов
- **M** — средняя сложность или требует небольшой backend-работы
- **L** — много компонентов/табов или значительная backend-работа
- **XL** — сложная страница с множеством зависимостей

**Статусы API:**
- **OK** — endpoint готов
- **NEEDS WORK** — требует detail serializer + slug lookup
- **NOT READY** — нет serializer_class
- **PLAN** — endpoint не реализован
- **N/A** — API не требуется

---

## Architecture Overview

### Frontend (Nuxt 3)

**Слои:**

```
Pages → Components → Composables → Stores → Utils
```

- **Pages** — роутинг, композиция, минимум логики
- **Components** — UI (Nuxt UI) + Domain компоненты
- **Composables** — бизнес-логика, API-вызовы
- **Stores** — глобальное состояние (auth + user data в `user.ts`)
- **Utils** — axios client, helpers

**Структура компонентов:**

```
components/
├── entity/                      # Domain компоненты
│   ├── EntityCard.vue           # Карточка для списков
│   ├── EntityList.vue           # Контейнер списка
│   ├── EntitySublist.vue        # Списки в табах деталей
│   ├── EntitySublistCard.vue    # Карточки в sublists
│   ├── EntityHeader.vue         # Шапка detail page
│   └── ReadingProgress.vue      # Прогресс чтения
├── info/                        # Info tab компоненты
│   ├── InfoTab.vue
│   ├── InfoPanel.vue
│   ├── TechInfoPanel.vue
│   └── Images.vue
├── ui/                          # Переиспользуемые UI
│   ├── Pagination.vue
│   ├── SortSelect.vue
│   ├── SearchInput.vue
│   └── FilterToggles.vue
└── common/                      # Общие
    ├── PageWithHeader.vue
    ├── UserMenu.vue
    └── NotificationsSlideover.vue
```

**State management:**

- `stores/user.ts` — данные пользователя + auth логика (login, logout, register, token refresh)
- URL query params как источник правды для списков (`?page=2&sort=-name`)
- Nested routes для табов деталей (`/characters/[slug]/issues`)

---

### Backend (Django)

**Data Flow:**

```
ComicVine API → Scrapy → MongoDB → Celery Tasks → PostgreSQL → DRF API
```

**Ключевые паттерны:**

- `ComicvineSyncModel` — базовый класс для всех comic-сущностей
- `utils/api/` — shared mixins, filters, pagination, permissions
- `<entity>/api/viewsets.py` + `serializers.py` — API для каждой сущности

**Pagination response:**

```json
{
  "count": 1234,
  "next": "...",
  "previous": "...",
  "pages_count": 42,
  "results": [...]
}
```

---

### Frontend ↔ Backend Integration

| Аспект | Решение |
|--------|---------|
| HTTP client | axios (useAxios composable) |
| Data fetching | Pinia Colada + axios |
| Auth | JWT в interceptor, auto token refresh на 401 |
| Pagination | `pages_count` уже в API response |
| API base URL | Вынести в `runtimeConfig` (TODO: сейчас hardcoded) |

**Error Handling (гибридный подход):**

```
axios interceptor (централизованно):
├── 401 → refresh token / redirect to login
├── 403 → toast "Access denied"
└── 500 → toast "Server error"

Pages/Components (per-request):
├── 400 → inline validation errors
├── 404 → error page / empty state
└── 422 → бизнес-логика
```

---

### Data Fetching (Pinia Colada)

**Библиотека:** [Pinia Colada](https://github.com/posva/pinia-colada) — официальная от автора Pinia.

**Структура composables:**

```
composables/
├── api/
│   ├── characters.ts      # characterKeys + useCharactersList + useCharacterDetail
│   ├── volumes.ts
│   ├── issues.ts
│   ├── publishers.ts
│   ├── concepts.ts
│   ├── locations.ts
│   ├── objects.ts
│   ├── people.ts
│   ├── powers.ts
│   ├── story-arcs.ts
│   ├── teams.ts
│   └── profile.ts
│
└── useAxios.ts            # HTTP client с interceptors
```

**Паттерн: Keys Factory + defineQuery (гибрид):**

```typescript
// composables/api/characters.ts

// Keys factory — для инвалидации и консистентности
export const characterKeys = {
  all: ['characters'] as const,
  lists: () => [...characterKeys.all, 'list'] as const,
  list: (params: object) => [...characterKeys.lists(), params] as const,
  details: () => [...characterKeys.all, 'detail'] as const,
  detail: (slug: string) => [...characterKeys.details(), slug] as const,
}

// Query definitions
export const useCharactersList = defineQuery(() => {
  const route = useRoute()
  const axios = useAxios()

  return {
    key: () => characterKeys.list(route.query),
    query: async (): Promise<PaginatedResponse<Character>> => {
      const { data } = await axios.get('/characters/', { params: route.query })
      return data
    },
    staleTime: 5 * 60 * 1000  // 5 минут
  }
})

export const useCharacterDetail = defineQuery(() => {
  const route = useRoute()
  const axios = useAxios()

  return {
    key: () => characterKeys.detail(route.params.slug as string),
    query: async (): Promise<Character> => {
      const { data } = await axios.get(`/characters/${route.params.slug}/`)
      return data
    },
    staleTime: 5 * 60 * 1000
  }
})
```

**Использование в pages:**

```typescript
// pages/characters/index.vue
const { data, status } = useCharactersList()

const items = computed(() =>
  data.value?.results.map(char => ({
    slug: char.slug,
    name: char.name,
    image: char.image ?? defaultImage,
    description: char.short_description,
    tags: [`${char.issues_count} issues`]
  })) ?? []
)
```

**Кэширование:**

| Тип данных | staleTime | gcTime | Примечание |
|------------|-----------|--------|------------|
| Списки сущностей | 5 min | 30 min | Данные обновляются раз в сутки |
| Детали сущности | 5 min | 30 min | Редко меняются |
| Счётчики (count) | 5 min | 30 min | Меняются при добавлении |
| Профиль / reading progress | 1 min | 30 min | Меняется при действиях пользователя |
| Technical info | 10 min | 30 min | Практически статичные |

**Инвалидация после мутаций:**

```typescript
const cache = useQueryCache()

// После mark as read
async function markAsRead(issueSlug: string) {
  await axios.post(`/issues/${issueSlug}/mark-read/`)

  cache.invalidateQueries({ key: issueKeys.detail(issueSlug) })
  cache.invalidateQueries({ key: volumeKeys.all })   // reading progress
  cache.invalidateQueries({ key: profileKeys.all })  // статистика
}

// Инвалидировать все данные сущности
cache.invalidateQueries({ key: characterKeys.all })
```

---

### Mutations (useMutation)

**Auth мутации** остаются в `stores/user.ts` — работает, не трогаем.

**User-facing и admin мутации** — через Pinia Colada `defineMutation`.

**Паттерн:**

```typescript
// composables/api/issues.ts

export const useMarkIssueRead = defineMutation(() => {
  const axios = useAxios()
  const cache = useQueryCache()
  const toast = useToast()

  return {
    mutation: async (issueSlug: string) => {
      await axios.post(`/issues/${issueSlug}/mark-read/`)
    },
    onSuccess: (_data, issueSlug) => {
      // Issue
      cache.invalidateQueries({ key: issueKeys.detail(issueSlug) })
      cache.invalidateQueries({ key: issueKeys.lists() })

      // Volume — reading progress + списки
      cache.invalidateQueries({ key: volumeKeys.all })

      // Story Arc — reading progress + списки
      cache.invalidateQueries({ key: storyArcKeys.all })

      // Profile — статистика
      cache.invalidateQueries({ key: profileKeys.all })

      // Все детальки с reading progress
      cache.invalidateQueries({ key: characterKeys.details() })
      cache.invalidateQueries({ key: conceptKeys.details() })
      cache.invalidateQueries({ key: locationKeys.details() })
      cache.invalidateQueries({ key: objectKeys.details() })
      cache.invalidateQueries({ key: personKeys.details() })
      cache.invalidateQueries({ key: publisherKeys.details() })
      cache.invalidateQueries({ key: teamKeys.details() })

      toast.add({ title: 'Marked as read', color: 'success' })
    },
    onError: (error) => {
      // 401/403/500 уже в axios interceptor
      toast.add({
        title: 'Failed to mark as read',
        description: error.message,
        color: 'error'
      })
    }
  }
})
```

**Использование:**

```vue
<script setup>
const { mutate: markRead, status } = useMarkIssueRead()
</script>

<template>
  <UButton
    @click="markRead(route.params.slug)"
    :loading="status === 'pending'"
  >
    Mark as Read
  </UButton>
</template>
```

**Watch/Unwatch** — локальная инвалидация:

```typescript
export const useStartWatch = defineMutation(() => {
  const axios = useAxios()
  const cache = useQueryCache()

  return {
    mutation: async ({ entityType, slug }: { entityType: string, slug: string }) => {
      await axios.post(`/${entityType}/${slug}/start-watch/`)
    },
    onSuccess: (_data, { entityType, slug }) => {
      const keys = getEntityKeys(entityType)
      cache.invalidateQueries({ key: keys.detail(slug) })
    }
  }
})
```

**Admin mutations** — инвалидация списка:

```typescript
export const useSkipIssue = defineMutation(() => {
  const axios = useAxios()
  const cache = useQueryCache()

  return {
    mutation: async (issueId: number) => {
      await axios.post(`/missing-issues/skip-issue/${issueId}/`)
    },
    onSuccess: () => {
      cache.invalidateQueries({ key: ['missing-issues'] })
    }
  }
})
```

**Стратегия обновления:** Pessimistic (ждём ответ сервера, показываем loading).

---

### Forms и валидация

**Библиотека:** Zod — популярный, хорошо типизированный.

**Организация схем:** Inline в компоненте (1 компонент = 1 схема, переиспользование не требуется).

**Серверные ошибки:** DRF возвращает 400 с форматом `{ "field": ["error message"] }`.

**Composable для обработки:**

```typescript
// composables/useFormErrors.ts
import { isAxiosError } from 'axios'
import type { FormError } from '#ui/types'

type FormInstance = { setErrors: (errors: FormError[]) => void }

export function useFormErrors(formRef: Ref<FormInstance | null>) {
  async function handleSubmit<T>(
    submitFn: () => Promise<T>
  ): Promise<T | undefined> {
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

**Использование:**

```vue
<script setup>
import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters')
})

const state = reactive({ email: '', password: '' })
const form = useTemplateRef('form')
const { handleSubmit } = useFormErrors(form)

async function onSubmit(data) {
  const result = await handleSubmit(() => login(data))
  if (result) {
    navigateTo('/dashboard')
  }
}
</script>

<template>
  <UForm ref="form" :schema="schema" :state="state" @submit="onSubmit">
    <UFormField name="email" label="Email">
      <UInput v-model="state.email" />
    </UFormField>
    <UFormField name="password" label="Password">
      <UInput v-model="state.password" type="password" />
    </UFormField>
    <UButton type="submit">Login</UButton>
  </UForm>
</template>
```

---

### TypeScript типы

**Подход:** Генерация из OpenAPI (API ещё меняется, типы должны быть в синхронизации).

**Инструменты:**
- `drf-spectacular` — генерация OpenAPI схемы из DRF
- `openapi-ts` — генерация TS интерфейсов (отдельные файлы)

**Установка:**

```bash
# Backend
pip install drf-spectacular

# Frontend
npm install -D @hey-api/openapi-ts
```

**npm scripts:**

```json
{
  "scripts": {
    "generate:types": "openapi-ts --input ../schema.yaml --output app/types/api",
    "generate:schema": "cd .. && python manage.py spectacular --file schema.yaml",
    "generate": "npm run generate:schema && npm run generate:types"
  }
}
```

**Структура:**

```
frontend/app/types/
├── api/                    # сгенерированные
│   ├── models/
│   │   ├── Character.ts
│   │   ├── CharacterDetail.ts
│   │   ├── Volume.ts
│   │   └── ...
│   └── index.ts
└── index.d.ts              # ручные типы (если нужны)
```

**Использование:**

```typescript
import type { Character, PaginatedCharacterList } from '~/types/api'

const { data } = await axios.get<PaginatedCharacterList>('/characters/')
```

**Workflow:** После изменения сериализаторов — `npm run generate`.

---

### SSR/SSG

**Стратегия:** SSR по умолчанию, CSR для приватных страниц.

| Страницы | Режим | Причина |
|----------|-------|---------|
| Списки сущностей | SSR | SEO, динамические данные |
| Детали сущностей | SSR | SEO |
| Поиск | SSR | SEO для результатов |
| Home | SSR | Персонализированные данные |
| Auth (login, register, reset) | CSR | Приватные |
| Profile | CSR | Приватные данные |
| Missing issues (admin) | CSR | Только для staff |

**Конфигурация:**

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  ssr: true,  // SSR по умолчанию

  routeRules: {
    '/users/**': { ssr: false },
    '/missing-issues/**': { ssr: false },
  }
})
```

---

### Error Handling UI

**Error pages:** Используем существующий `error.vue` с `UError` из Nuxt UI.

**Toast уведомления (в axios interceptor):**

| Ошибка | UI |
|--------|-----|
| 401 Unauthorized | redirect to login |
| 403 Forbidden | toast "Access denied" |
| 500 Server Error | toast "Server error" |
| Network Error | toast "Connection lost" |

**Inline ошибки форм:** Через `useFormErrors` composable.

---

### Environment Config

**runtimeConfig для API URL:**

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

```typescript
// composables/useAxios.ts
export function useAxios() {
  const config = useRuntimeConfig()

  const axiosIns = axios.create({
    baseURL: config.public.apiBase
  })
  // ...
}
```

**Переменные окружения:**

```bash
# .env.development
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api

# .env.production
NUXT_PUBLIC_API_BASE=https://readcomics.net/api
```

---

### SEO

**Базовый подход с useSeoMeta:**

```vue
<!-- pages/characters/[slug].vue -->
<script setup>
const character = inject('character')

useSeoMeta({
  title: () => character.value?.name ?? 'Character',
  description: () => character.value?.short_description,
  ogImage: () => character.value?.image,
  ogType: 'website'
})
</script>
```

**Для списков:**

```vue
<!-- pages/characters/index.vue -->
<script setup>
useSeoMeta({
  title: 'Characters',
  description: 'Browse all comic book characters'
})
</script>
```

---

### Testing

#### Frontend

| Слой | Инструмент | Приоритет |
|------|------------|-----------|
| Composables | Vitest | Высокий |
| Components | Vitest + Vue Test Utils | Средний |
| E2E | Playwright | Низкий (позже) |

#### Backend

**Структура файлов:**

```
<app>/tests/
├── conftest.py          # Entity-specific fixtures
├── factories.py         # Factory Boy factories
├── test_drf_urls.py     # URL resolution tests
└── test_e2e.py          # E2E endpoint tests
```

**Глобальные fixtures** (`read_comics/conftest.py`):
- `api_client` — анонимный APIClient
- `authenticated_api_client` — JWT обычного пользователя
- `staff_api_client` — JWT staff
- `superuser_api_client` — JWT superuser

**test_drf_urls.py — URL Resolution:**

```python
class TestCharactersApiUrls:
    @staticmethod
    def test_list() -> None:
        assert reverse("api:character-list") == "/api/characters/"
        assert resolve("/api/characters/").view_name == "api:character-list"
```

**test_e2e.py — E2E Endpoint Tests:**

| Категория | Что проверяем |
|-----------|---------------|
| Count | `/count/` endpoint с фильтрами |
| List | Response keys, data, ordering, pagination |
| Detail | Все поля, 404 для несуществующих |
| TechnicalInfo | Permissions (401, 403 для non-staff) |
| EdgeCases | Boundary conditions (page=0, page=-1) |
| Consistency | List vs Detail, List vs Count |
| HTTPMethods | POST/PUT/PATCH/DELETE rejection |

**Паттерн теста:**

```python
pytestmark = pytest.mark.django_db

class TestCharactersList:
    list_keys = {"slug", "image", "name", ...}

    def test_data(self, api_client: APIClient, character_with_issues: Character) -> None:
        response = api_client.get("/api/characters/")
        assert response.status_code == 200
        assert response.data["results"][0]["slug"] == character_with_issues.slug
```

**Permissions testing:**

```python
class TestCharacterTechnicalInfo:
    @staticmethod
    def test_no_auth(api_client, character) -> None:
        response = api_client.get(f"/api/characters/{character.slug}/technical-info/")
        assert response.status_code == 401

    @staticmethod
    def test_staff(staff_api_client, character) -> None:
        response = staff_api_client.get(...)
        assert response.status_code == 200
```

---

## Phase 1: Auth

**Backend работа:** Нет (все endpoints готовы)

| № | Задача | Сложность | Зависимости | Статус |
|---|--------|-----------|-------------|--------|
| 1.1 | Login page [RC-257](https://nonameitem.atlassian.net/browse/RC-257) | S | — | DONE |
| 1.2 | Registration page [RC-258](https://nonameitem.atlassian.net/browse/RC-258) | S | — | DONE |
| 1.3 | Password reset request [RC-261](https://nonameitem.atlassian.net/browse/RC-261) | S | — | TODO |
| 1.4 | Password reset confirm [RC-262](https://nonameitem.atlassian.net/browse/RC-262) | S | 1.3 | TODO |
| 1.5 | Logout [RC-264](https://nonameitem.atlassian.net/browse/RC-264) | S | 1.1 | DONE |

**Итого Phase 1:** 5 задач, 3 done, 2 todo

---

## Phase 1.5: User Profile

**Backend работа:** Нет (endpoint готов)

| № | Задача | Сложность | Зависимости | Статус |
|---|--------|-----------|-------------|--------|
| 1.5.1 | User profile [RC-263](https://nonameitem.atlassian.net/browse/RC-263) | M | 1.1 | TODO |

**Итого Phase 1.5:** 1 задача

---

## Phase 2: Home & Dashboard

**Backend работа:**
- `/api/issues/update-history/` [PLAN]
- `/api/issues/by-date/<year>/<month>/<day>/` [PLAN]

### 2.1 Home page [RC-8](https://nonameitem.atlassian.net/browse/RC-8) | Сложность: **L**

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 2.1.1 | Reading progress | /api/profile/finished-stats/ | OK | [RC-28](https://nonameitem.atlassian.net/browse/RC-28) |
| 2.1.2 | Unfinished volumes | /api/volumes/started/ | OK | [RC-29](https://nonameitem.atlassian.net/browse/RC-29) |
| 2.1.3 | Unfinished story arcs | /api/story-arcs/started/ | OK | [RC-30](https://nonameitem.atlassian.net/browse/RC-30) |
| 2.1.4 | Counter cards | /api/characters/count/, /api/issues/count/ | OK | [RC-31](https://nonameitem.atlassian.net/browse/RC-31) |
| 2.1.5 | Update history | /api/issues/update-history/ | **PLAN** | [RC-32](https://nonameitem.atlassian.net/browse/RC-32) |

### 2.2 New issues by day [RC-164](https://nonameitem.atlassian.net/browse/RC-164) | Сложность: **M**

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 2.2.1 | Page data | /api/issues/by-date/\<year\>/\<month\>/\<day\>/ | **PLAN** | [RC-171](https://nonameitem.atlassian.net/browse/RC-171) |

**Итого Phase 2:** 2 задачи, 2 backend endpoints

---

## Phase 3: Entity Lists

**Backend работа:** Нет (все API готовы)

| № | Задача | Сложность | Зависимости | Endpoint | Статус |
|---|--------|-----------|-------------|----------|--------|
| 3.1 | Publishers list [RC-15](https://nonameitem.atlassian.net/browse/RC-15) | S | — | /api/publishers/ [OK] | TODO |
| 3.2 | Characters list [RC-4](https://nonameitem.atlassian.net/browse/RC-4) | S | — | /api/characters/ [OK] | TODO |
| 3.3 | Volumes list [RC-21](https://nonameitem.atlassian.net/browse/RC-21) | S | — | /api/volumes/ [OK] | TODO |
| 3.4 | Issues list [RC-6](https://nonameitem.atlassian.net/browse/RC-6) | S | — | /api/issues/ [OK] | TODO |
| 3.5 | Story arcs list [RC-17](https://nonameitem.atlassian.net/browse/RC-17) | S | — | /api/story-arcs/ [OK] | TODO |
| 3.6 | Teams list [RC-19](https://nonameitem.atlassian.net/browse/RC-19) | S | — | /api/teams/ [OK] | TODO |
| 3.7 | People list [RC-13](https://nonameitem.atlassian.net/browse/RC-13) | S | — | /api/people/ [OK] | TODO |
| 3.8 | Concepts list [RC-2](https://nonameitem.atlassian.net/browse/RC-2) | S | — | /api/concepts/ [OK] | TODO |
| 3.9 | Locations list [RC-9](https://nonameitem.atlassian.net/browse/RC-9) | S | — | /api/locations/ [OK] | TODO |
| 3.10 | Objects list [RC-11](https://nonameitem.atlassian.net/browse/RC-11) | S | — | /api/objects/ [OK] | TODO |
| 3.11 | Volumes continue reading [RC-165](https://nonameitem.atlassian.net/browse/RC-165) | S | 1.1 | /api/volumes/started/ [OK] | TODO |
| 3.12 | Story arcs continue reading [RC-166](https://nonameitem.atlassian.net/browse/RC-166) | S | 1.1 | /api/story-arcs/started/ [OK] | TODO |

**Рекомендация:** Сделать первый list (например 3.2 Characters) как шаблон, потом остальные пойдут быстро — общие компоненты (пагинация, фильтры, карточки).

**Итого Phase 3:** 12 задач, все S, все API готовы

---

## Phase 4: Entity Details

### Phase 4.1: Details с готовым API

Основной detail endpoint готов, но nested endpoints (табы) требуют backend работы.

#### 4.1 Character detail [RC-5](https://nonameitem.atlassian.net/browse/RC-5) | Сложность: **XL**

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.1.1 | Header + Tab selector | /api/characters/\<slug\>/ | OK | [RC-198](https://nonameitem.atlassian.net/browse/RC-198) |
| 4.1.2 | Reading progress | /api/characters/\<slug\>/ | OK | [RC-199](https://nonameitem.atlassian.net/browse/RC-199) |
| 4.1.3 | Main info tab | /api/characters/\<slug\>/ | OK | [RC-34](https://nonameitem.atlassian.net/browse/RC-34) |
| 4.1.4 | Technical info tab | /api/characters/\<slug\>/technical-info/ | OK | [RC-35](https://nonameitem.atlassian.net/browse/RC-35) |
| 4.1.5 | Issues tab | /api/characters/\<slug\>/issues/ | **PLAN** | [RC-36](https://nonameitem.atlassian.net/browse/RC-36) |
| 4.1.6 | Volumes tab | /api/characters/\<slug\>/volumes/ | **PLAN** | [RC-37](https://nonameitem.atlassian.net/browse/RC-37) |
| 4.1.7 | Died in tab | /api/characters/\<slug\>/died-in-issues/ | **PLAN** | [RC-39](https://nonameitem.atlassian.net/browse/RC-39) |
| 4.1.8 | Authors tab | /api/characters/\<slug\>/authors/ | **PLAN** | [RC-38](https://nonameitem.atlassian.net/browse/RC-38) |
| 4.1.9 | Friends tab | /api/characters/\<slug\>/friends/ | **PLAN** | [RC-40](https://nonameitem.atlassian.net/browse/RC-40) |
| 4.1.10 | Enemies tab | /api/characters/\<slug\>/enemies/ | **PLAN** | [RC-41](https://nonameitem.atlassian.net/browse/RC-41) |
| 4.1.11 | Teams tab | /api/characters/\<slug\>/teams/ | **PLAN** | [RC-42](https://nonameitem.atlassian.net/browse/RC-42) |
| 4.1.12 | Team friends tab | /api/characters/\<slug\>/team-friends/ | **PLAN** | [RC-43](https://nonameitem.atlassian.net/browse/RC-43) |
| 4.1.13 | Team enemies tab | /api/characters/\<slug\>/team-enemies/ | **PLAN** | [RC-44](https://nonameitem.atlassian.net/browse/RC-44) |
| 4.1.14 | Start/stop watch | /api/characters/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-52](https://nonameitem.atlassian.net/browse/RC-52) |
| 4.1.15 | Download | Django only | N/A | [RC-51](https://nonameitem.atlassian.net/browse/RC-51) |
| 4.1.16 | Missing issues link (staff) | — | N/A | [RC-53](https://nonameitem.atlassian.net/browse/RC-53) |

**Backend: 11 endpoints PLAN**

#### 4.2 Concept detail [RC-3](https://nonameitem.atlassian.net/browse/RC-3) | Сложность: **L**

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.2.1 | Header + Tab selector | /api/concepts/\<slug\>/ | OK | [RC-200](https://nonameitem.atlassian.net/browse/RC-200) |
| 4.2.2 | Reading progress | /api/concepts/\<slug\>/ | OK | [RC-201](https://nonameitem.atlassian.net/browse/RC-201) |
| 4.2.3 | Main info tab | /api/concepts/\<slug\>/ | OK | [RC-33](https://nonameitem.atlassian.net/browse/RC-33) |
| 4.2.4 | Technical info tab | /api/concepts/\<slug\>/technical-info/ | OK | [RC-45](https://nonameitem.atlassian.net/browse/RC-45) |
| 4.2.5 | Issues tab | /api/concepts/\<slug\>/issues/ | **PLAN** | [RC-46](https://nonameitem.atlassian.net/browse/RC-46) |
| 4.2.6 | Volumes tab | /api/concepts/\<slug\>/volumes/ | **PLAN** | [RC-47](https://nonameitem.atlassian.net/browse/RC-47) |
| 4.2.7 | Start/stop watch | /api/concepts/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-49](https://nonameitem.atlassian.net/browse/RC-49) |
| 4.2.8 | Download | Django only | N/A | [RC-48](https://nonameitem.atlassian.net/browse/RC-48) |
| 4.2.9 | Missing issues link (staff) | — | N/A | [RC-50](https://nonameitem.atlassian.net/browse/RC-50) |

**Backend: 4 endpoints PLAN**

#### 4.3 Issue detail [RC-7](https://nonameitem.atlassian.net/browse/RC-7) | Сложность: **XL**

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.3.1 | Header + Tab selector | /api/issues/\<slug\>/ | OK | [RC-225](https://nonameitem.atlassian.net/browse/RC-225) |
| 4.3.2 | Reading progress (volume) | /api/volumes/\<slug\>/ | **NEEDS WORK** | [RC-226](https://nonameitem.atlassian.net/browse/RC-226) |
| 4.3.3 | Main info tab | /api/issues/\<slug\>/ | OK | [RC-54](https://nonameitem.atlassian.net/browse/RC-54) |
| 4.3.4 | Technical info tab | /api/issues/\<slug\>/technical-info/ | OK | [RC-55](https://nonameitem.atlassian.net/browse/RC-55) |
| 4.3.5 | Characters tab | /api/issues/\<slug\>/characters/ | **PLAN** | [RC-56](https://nonameitem.atlassian.net/browse/RC-56) |
| 4.3.6 | Authors tab | /api/issues/\<slug\>/authors/ | **PLAN** | [RC-57](https://nonameitem.atlassian.net/browse/RC-57) |
| 4.3.7 | First appearances tab | /api/issues/\<slug\>/first-appearances/ | **PLAN** | [RC-58](https://nonameitem.atlassian.net/browse/RC-58) |
| 4.3.8 | Characters died tab | /api/issues/\<slug\>/characters-died/ | **PLAN** | [RC-59](https://nonameitem.atlassian.net/browse/RC-59) |
| 4.3.9 | Concepts tab | /api/issues/\<slug\>/concepts/ | **PLAN** | [RC-60](https://nonameitem.atlassian.net/browse/RC-60) |
| 4.3.10 | Locations tab | /api/issues/\<slug\>/locations/ | **PLAN** | [RC-61](https://nonameitem.atlassian.net/browse/RC-61) |
| 4.3.11 | Objects tab | /api/issues/\<slug\>/objects/ | **PLAN** | [RC-62](https://nonameitem.atlassian.net/browse/RC-62) |
| 4.3.12 | Story arcs tab | /api/issues/\<slug\>/story-arcs/ | **PLAN** | [RC-63](https://nonameitem.atlassian.net/browse/RC-63) |
| 4.3.13 | Teams tab | /api/issues/\<slug\>/teams/ | **PLAN** | [RC-64](https://nonameitem.atlassian.net/browse/RC-64) |
| 4.3.14 | Disbanded teams tab | /api/issues/\<slug\>/disbanded-teams/ | **PLAN** | [RC-65](https://nonameitem.atlassian.net/browse/RC-65) |
| 4.3.15 | Mark read | /api/issues/\<slug\>/mark-read/ | **PLAN** | [RC-71](https://nonameitem.atlassian.net/browse/RC-71) |
| 4.3.16 | Previous/Next | /api/issues/\<slug\>/ | OK | [RC-69](https://nonameitem.atlassian.net/browse/RC-69) |
| 4.3.17 | Download | Django only | N/A | [RC-68](https://nonameitem.atlassian.net/browse/RC-68) |

**Backend: 11 endpoints PLAN + 1 NEEDS WORK (volume detail для progress)**

#### 4.4 Location detail [RC-10](https://nonameitem.atlassian.net/browse/RC-10) | Сложность: **L**

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.4.1 | Header + Tab selector | /api/locations/\<slug\>/ | OK | [RC-202](https://nonameitem.atlassian.net/browse/RC-202) |
| 4.4.2 | Reading progress | /api/locations/\<slug\>/ | OK | [RC-203](https://nonameitem.atlassian.net/browse/RC-203) |
| 4.4.3 | Main info tab | /api/locations/\<slug\>/ | OK | [RC-72](https://nonameitem.atlassian.net/browse/RC-72) |
| 4.4.4 | Technical info tab | /api/locations/\<slug\>/technical-info/ | OK | [RC-73](https://nonameitem.atlassian.net/browse/RC-73) |
| 4.4.5 | Issues tab | /api/locations/\<slug\>/issues/ | **PLAN** | [RC-74](https://nonameitem.atlassian.net/browse/RC-74) |
| 4.4.6 | Volumes tab | /api/locations/\<slug\>/volumes/ | **PLAN** | [RC-75](https://nonameitem.atlassian.net/browse/RC-75) |
| 4.4.7 | Start/stop watch | /api/locations/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-77](https://nonameitem.atlassian.net/browse/RC-77) |
| 4.4.8 | Download | Django only | N/A | [RC-76](https://nonameitem.atlassian.net/browse/RC-76) |
| 4.4.9 | Missing issues link (staff) | — | N/A | [RC-78](https://nonameitem.atlassian.net/browse/RC-78) |

**Backend: 4 endpoints PLAN**

#### Сводка Phase 4.1-4.4

| № | Entity | Сложность | Backend PLAN | Backend NEEDS WORK |
|---|--------|-----------|--------------|-------------------|
| 4.1 | Character | XL | 11 | — |
| 4.2 | Concept | L | 4 | — |
| 4.3 | Issue | XL | 11 | 1 (volume detail) |
| 4.4 | Location | L | 4 | — |
| — | **Итого** | — | **30** | **1** |

---

### Phase 4.5-4.10: Details требующие backend

Эти сущности требуют сначала backend работу: detail serializer + slug lookup.

#### 4.5 Object detail [RC-12](https://nonameitem.atlassian.net/browse/RC-12) | Сложность: **L**

**Блокер:** /api/objects/\<slug\>/ [NEEDS WORK — detail serializer + slug lookup]

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.5.1 | Header + Tab selector | /api/objects/\<slug\>/ | **NEEDS WORK** | [RC-204](https://nonameitem.atlassian.net/browse/RC-204) |
| 4.5.2 | Reading progress | /api/objects/\<slug\>/ | **NEEDS WORK** | [RC-205](https://nonameitem.atlassian.net/browse/RC-205) |
| 4.5.3 | Main info tab | /api/objects/\<slug\>/ | **NEEDS WORK** | [RC-79](https://nonameitem.atlassian.net/browse/RC-79) |
| 4.5.4 | Technical info tab | /api/objects/\<slug\>/technical-info/ | **PLAN** | [RC-80](https://nonameitem.atlassian.net/browse/RC-80) |
| 4.5.5 | Issues tab | /api/objects/\<slug\>/issues/ | **PLAN** | [RC-81](https://nonameitem.atlassian.net/browse/RC-81) |
| 4.5.6 | Volumes tab | /api/objects/\<slug\>/volumes/ | **PLAN** | [RC-82](https://nonameitem.atlassian.net/browse/RC-82) |
| 4.5.7 | Start/stop watch | /api/objects/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-83](https://nonameitem.atlassian.net/browse/RC-83) |
| 4.5.8 | Download | Django only | N/A | [RC-84](https://nonameitem.atlassian.net/browse/RC-84) |
| 4.5.9 | Missing issues link (staff) | — | N/A | [RC-206](https://nonameitem.atlassian.net/browse/RC-206) |

**Backend: 1 NEEDS WORK + 5 PLAN**

#### 4.6 Person detail [RC-14](https://nonameitem.atlassian.net/browse/RC-14) | Сложность: **L**

**Блокер:** /api/people/\<slug\>/ [NEEDS WORK — detail serializer + slug lookup]

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.6.1 | Header + Tab selector | /api/people/\<slug\>/ | **NEEDS WORK** | [RC-207](https://nonameitem.atlassian.net/browse/RC-207) |
| 4.6.2 | Reading progress | /api/people/\<slug\>/ | **NEEDS WORK** | [RC-208](https://nonameitem.atlassian.net/browse/RC-208) |
| 4.6.3 | Main info tab | /api/people/\<slug\>/ | **NEEDS WORK** | [RC-85](https://nonameitem.atlassian.net/browse/RC-85) |
| 4.6.4 | Technical info tab | /api/people/\<slug\>/technical-info/ | **PLAN** | [RC-86](https://nonameitem.atlassian.net/browse/RC-86) |
| 4.6.5 | Issues tab | /api/people/\<slug\>/issues/ | **PLAN** | [RC-87](https://nonameitem.atlassian.net/browse/RC-87) |
| 4.6.6 | Volumes tab | /api/people/\<slug\>/volumes/ | **PLAN** | [RC-88](https://nonameitem.atlassian.net/browse/RC-88) |
| 4.6.7 | Characters tab | /api/people/\<slug\>/characters/ | **PLAN** | [RC-89](https://nonameitem.atlassian.net/browse/RC-89) |
| 4.6.8 | Start/stop watch | /api/people/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-91](https://nonameitem.atlassian.net/browse/RC-91) |
| 4.6.9 | Download | Django only | N/A | [RC-90](https://nonameitem.atlassian.net/browse/RC-90) |
| 4.6.10 | Missing issues link (staff) | — | N/A | [RC-209](https://nonameitem.atlassian.net/browse/RC-209) |

**Backend: 1 NEEDS WORK + 6 PLAN**

#### 4.7 Publisher detail [RC-16](https://nonameitem.atlassian.net/browse/RC-16) | Сложность: **L**

**Блокер:** /api/publishers/\<slug\>/ [NEEDS WORK — detail serializer + slug lookup]

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.7.1 | Header + Tab selector | /api/publishers/\<slug\>/ | **NEEDS WORK** | [RC-210](https://nonameitem.atlassian.net/browse/RC-210) |
| 4.7.2 | Reading progress | /api/publishers/\<slug\>/ | **NEEDS WORK** | [RC-211](https://nonameitem.atlassian.net/browse/RC-211) |
| 4.7.3 | Main info tab | /api/publishers/\<slug\>/ | **NEEDS WORK** | [RC-92](https://nonameitem.atlassian.net/browse/RC-92) |
| 4.7.4 | Technical info tab | /api/publishers/\<slug\>/technical-info/ | **PLAN** | [RC-93](https://nonameitem.atlassian.net/browse/RC-93) |
| 4.7.5 | Issues tab | /api/publishers/\<slug\>/issues/ | **PLAN** | [RC-94](https://nonameitem.atlassian.net/browse/RC-94) |
| 4.7.6 | Volumes tab | /api/publishers/\<slug\>/volumes/ | **PLAN** | [RC-95](https://nonameitem.atlassian.net/browse/RC-95) |
| 4.7.7 | Characters tab | /api/publishers/\<slug\>/characters/ | **PLAN** | [RC-96](https://nonameitem.atlassian.net/browse/RC-96) |
| 4.7.8 | Story arcs tab | /api/publishers/\<slug\>/story-arcs/ | **PLAN** | [RC-97](https://nonameitem.atlassian.net/browse/RC-97) |
| 4.7.9 | Teams tab | /api/publishers/\<slug\>/teams/ | **PLAN** | [RC-98](https://nonameitem.atlassian.net/browse/RC-98) |
| 4.7.10 | Start/stop watch | /api/publishers/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-100](https://nonameitem.atlassian.net/browse/RC-100) |
| 4.7.11 | Download | Django only | N/A | [RC-99](https://nonameitem.atlassian.net/browse/RC-99) |
| 4.7.12 | Missing issues link (staff) | — | N/A | [RC-212](https://nonameitem.atlassian.net/browse/RC-212) |

**Backend: 1 NEEDS WORK + 8 PLAN**

#### 4.8 Story Arc detail [RC-18](https://nonameitem.atlassian.net/browse/RC-18) | Сложность: **XL**

**Блокер:** /api/story-arcs/\<slug\>/ [NEEDS WORK — detail serializer + slug lookup]

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.8.1 | Header + Tab selector | /api/story-arcs/\<slug\>/ | **NEEDS WORK** | [RC-213](https://nonameitem.atlassian.net/browse/RC-213) |
| 4.8.2 | Reading progress | /api/story-arcs/\<slug\>/ | **NEEDS WORK** | [RC-214](https://nonameitem.atlassian.net/browse/RC-214) |
| 4.8.3 | Main info tab | /api/story-arcs/\<slug\>/ | **NEEDS WORK** | [RC-101](https://nonameitem.atlassian.net/browse/RC-101) |
| 4.8.4 | Technical info tab | /api/story-arcs/\<slug\>/technical-info/ | **PLAN** | [RC-102](https://nonameitem.atlassian.net/browse/RC-102) |
| 4.8.5 | Issues tab | /api/story-arcs/\<slug\>/issues/ | **PLAN** | [RC-103](https://nonameitem.atlassian.net/browse/RC-103) |
| 4.8.6 | Volumes tab | /api/story-arcs/\<slug\>/volumes/ | **PLAN** | [RC-104](https://nonameitem.atlassian.net/browse/RC-104) |
| 4.8.7 | First appearances tab | /api/story-arcs/\<slug\>/first-appearances/ | **PLAN** | [RC-105](https://nonameitem.atlassian.net/browse/RC-105) |
| 4.8.8 | Characters tab | /api/story-arcs/\<slug\>/characters/ | **PLAN** | [RC-106](https://nonameitem.atlassian.net/browse/RC-106) |
| 4.8.9 | Died tab | /api/story-arcs/\<slug\>/died/ | **PLAN** | [RC-107](https://nonameitem.atlassian.net/browse/RC-107) |
| 4.8.10 | Concepts tab | /api/story-arcs/\<slug\>/concepts/ | **PLAN** | [RC-108](https://nonameitem.atlassian.net/browse/RC-108) |
| 4.8.11 | Locations tab | /api/story-arcs/\<slug\>/locations/ | **PLAN** | [RC-109](https://nonameitem.atlassian.net/browse/RC-109) |
| 4.8.12 | Objects tab | /api/story-arcs/\<slug\>/objects/ | **PLAN** | [RC-110](https://nonameitem.atlassian.net/browse/RC-110) |
| 4.8.13 | Authors tab | /api/story-arcs/\<slug\>/authors/ | **PLAN** | [RC-111](https://nonameitem.atlassian.net/browse/RC-111) |
| 4.8.14 | Teams tab | /api/story-arcs/\<slug\>/teams/ | **PLAN** | [RC-112](https://nonameitem.atlassian.net/browse/RC-112) |
| 4.8.15 | Disbanded tab | /api/story-arcs/\<slug\>/disbanded/ | **PLAN** | [RC-113](https://nonameitem.atlassian.net/browse/RC-113) |
| 4.8.16 | Mark finished | /api/story-arcs/\<slug\>/mark-finished/ | **PLAN** | [RC-114](https://nonameitem.atlassian.net/browse/RC-114) |
| 4.8.17 | Start/stop watch | /api/story-arcs/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-116](https://nonameitem.atlassian.net/browse/RC-116) |
| 4.8.18 | Download | Django only | N/A | [RC-115](https://nonameitem.atlassian.net/browse/RC-115) |
| 4.8.19 | Missing issues link (staff) | — | N/A | [RC-215](https://nonameitem.atlassian.net/browse/RC-215) |

**Backend: 1 NEEDS WORK + 15 PLAN**

#### 4.9 Team detail [RC-20](https://nonameitem.atlassian.net/browse/RC-20) | Сложность: **L**

**Блокер:** /api/teams/\<slug\>/ [NEEDS WORK — detail serializer + slug lookup]

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.9.1 | Header + Tab selector | /api/teams/\<slug\>/ | **NEEDS WORK** | [RC-216](https://nonameitem.atlassian.net/browse/RC-216) |
| 4.9.2 | Reading progress | /api/teams/\<slug\>/ | **NEEDS WORK** | [RC-217](https://nonameitem.atlassian.net/browse/RC-217) |
| 4.9.3 | Main info tab | /api/teams/\<slug\>/ | **NEEDS WORK** | [RC-119](https://nonameitem.atlassian.net/browse/RC-119) |
| 4.9.4 | Technical info tab | /api/teams/\<slug\>/technical-info/ | **PLAN** | [RC-120](https://nonameitem.atlassian.net/browse/RC-120) |
| 4.9.5 | Issues tab | /api/teams/\<slug\>/issues/ | **PLAN** | [RC-121](https://nonameitem.atlassian.net/browse/RC-121) |
| 4.9.6 | Volumes tab | /api/teams/\<slug\>/volumes/ | **PLAN** | [RC-122](https://nonameitem.atlassian.net/browse/RC-122) |
| 4.9.7 | Members tab | /api/teams/\<slug\>/characters/ | **PLAN** | [RC-123](https://nonameitem.atlassian.net/browse/RC-123) |
| 4.9.8 | Enemies tab | /api/teams/\<slug\>/enemies/ | **PLAN** | [RC-124](https://nonameitem.atlassian.net/browse/RC-124) |
| 4.9.9 | Friends tab | /api/teams/\<slug\>/friends/ | **PLAN** | [RC-125](https://nonameitem.atlassian.net/browse/RC-125) |
| 4.9.10 | Disbanded in issues tab | /api/teams/\<slug\>/disbanded-in/ | **PLAN** | [RC-126](https://nonameitem.atlassian.net/browse/RC-126) |
| 4.9.11 | Start/stop watch | /api/teams/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-128](https://nonameitem.atlassian.net/browse/RC-128) |
| 4.9.12 | Download | Django only | N/A | [RC-127](https://nonameitem.atlassian.net/browse/RC-127) |
| 4.9.13 | Missing issues link (staff) | — | N/A | [RC-218](https://nonameitem.atlassian.net/browse/RC-218) |

**Backend: 1 NEEDS WORK + 9 PLAN**

#### 4.10 Volume detail [RC-22](https://nonameitem.atlassian.net/browse/RC-22) | Сложность: **XL**

**Блокер:** /api/volumes/\<slug\>/ [NEEDS WORK — detail serializer + slug lookup]

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 4.10.1 | Header + Tab selector | /api/volumes/\<slug\>/ | **NEEDS WORK** | [RC-219](https://nonameitem.atlassian.net/browse/RC-219) |
| 4.10.2 | Reading progress | /api/volumes/\<slug\>/ | **NEEDS WORK** | [RC-220](https://nonameitem.atlassian.net/browse/RC-220) |
| 4.10.3 | Main info tab | /api/volumes/\<slug\>/ | **NEEDS WORK** | [RC-221](https://nonameitem.atlassian.net/browse/RC-221) |
| 4.10.4 | Technical info tab | /api/volumes/\<slug\>/technical-info/ | **PLAN** | [RC-222](https://nonameitem.atlassian.net/browse/RC-222) |
| 4.10.5 | Issues tab | /api/volumes/\<slug\>/issues/ | **PLAN** | [RC-129](https://nonameitem.atlassian.net/browse/RC-129) |
| 4.10.6 | First appearances tab | /api/volumes/\<slug\>/first-appearances/ | **PLAN** | [RC-130](https://nonameitem.atlassian.net/browse/RC-130) |
| 4.10.7 | Characters tab | /api/volumes/\<slug\>/characters/ | **PLAN** | [RC-131](https://nonameitem.atlassian.net/browse/RC-131) |
| 4.10.8 | Characters died tab | /api/volumes/\<slug\>/died/ | **PLAN** | [RC-132](https://nonameitem.atlassian.net/browse/RC-132) |
| 4.10.9 | Concepts tab | /api/volumes/\<slug\>/concepts/ | **PLAN** | [RC-133](https://nonameitem.atlassian.net/browse/RC-133) |
| 4.10.10 | Locations tab | /api/volumes/\<slug\>/locations/ | **PLAN** | [RC-134](https://nonameitem.atlassian.net/browse/RC-134) |
| 4.10.11 | Objects tab | /api/volumes/\<slug\>/objects/ | **PLAN** | [RC-135](https://nonameitem.atlassian.net/browse/RC-135) |
| 4.10.12 | Authors tab | /api/volumes/\<slug\>/authors/ | **PLAN** | [RC-136](https://nonameitem.atlassian.net/browse/RC-136) |
| 4.10.13 | Story arcs tab | /api/volumes/\<slug\>/story-arcs/ | **PLAN** | [RC-137](https://nonameitem.atlassian.net/browse/RC-137) |
| 4.10.14 | Teams tab | /api/volumes/\<slug\>/teams/ | **PLAN** | [RC-138](https://nonameitem.atlassian.net/browse/RC-138) |
| 4.10.15 | Disbanded tab | /api/volumes/\<slug\>/disbanded/ | **PLAN** | [RC-139](https://nonameitem.atlassian.net/browse/RC-139) |
| 4.10.16 | Mark finished | /api/volumes/\<slug\>/mark-finished/ | **PLAN** | [RC-224](https://nonameitem.atlassian.net/browse/RC-224) |
| 4.10.17 | Start/stop watch | /api/volumes/\<slug\>/start-watch/, stop-watch/ | **PLAN** | [RC-142](https://nonameitem.atlassian.net/browse/RC-142) |
| 4.10.18 | Download | Django only | N/A | [RC-140](https://nonameitem.atlassian.net/browse/RC-140) |
| 4.10.19 | Missing issues link (staff) | — | N/A | [RC-223](https://nonameitem.atlassian.net/browse/RC-223) |

**Backend: 1 NEEDS WORK + 15 PLAN**

#### Сводка Phase 4.5-4.10

| № | Entity | Сложность | NEEDS WORK | PLAN |
|---|--------|-----------|------------|------|
| 4.5 | Object | L | 1 | 5 |
| 4.6 | Person | L | 1 | 6 |
| 4.7 | Publisher | L | 1 | 8 |
| 4.8 | Story Arc | XL | 1 | 15 |
| 4.9 | Team | L | 1 | 9 |
| 4.10 | Volume | XL | 1 | 15 |
| — | **Итого** | — | **6** | **58** |

**Рекомендация по порядку:** 4.10 Volume первым (блокирует 4.3.2 Issue reading progress), затем остальные.

---

### Phase 4.11-4.19: Nested Issue Details

Issue detail страницы в контексте родительской сущности — для prev/next навигации внутри подсписка.

| № | Задача | Сложность | Parent | Зависимости | Jira |
|---|--------|-----------|--------|-------------|------|
| 4.11 | Character Issue detail [RC-153](https://nonameitem.atlassian.net/browse/RC-153) | M | 4.1 | 4.3; 4.1 OK | TODO |
| 4.12 | Concept Issue detail [RC-154](https://nonameitem.atlassian.net/browse/RC-154) | M | 4.2 | 4.3; 4.2 OK | TODO |
| 4.13 | Location Issue detail [RC-155](https://nonameitem.atlassian.net/browse/RC-155) | M | 4.4 | 4.3; 4.4 OK | TODO |
| 4.14 | Object Issue detail [RC-156](https://nonameitem.atlassian.net/browse/RC-156) | M | 4.5 | 4.3; 4.5 **NEEDS WORK** | TODO |
| 4.15 | Person Issue detail [RC-157](https://nonameitem.atlassian.net/browse/RC-157) | M | 4.6 | 4.3; 4.6 **NEEDS WORK** | TODO |
| 4.16 | Publisher Issue detail [RC-158](https://nonameitem.atlassian.net/browse/RC-158) | M | 4.7 | 4.3; 4.7 **NEEDS WORK** | TODO |
| 4.17 | Story Arc Issue detail [RC-159](https://nonameitem.atlassian.net/browse/RC-159) | M | 4.8 | 4.3; 4.8 **NEEDS WORK** | TODO |
| 4.18 | Team Issue detail [RC-160](https://nonameitem.atlassian.net/browse/RC-160) | M | 4.9 | 4.3; 4.9 **NEEDS WORK** | TODO |
| 4.19 | Volume Issue detail [RC-161](https://nonameitem.atlassian.net/browse/RC-161) | M | 4.10 | 4.3; 4.10 **NEEDS WORK** | TODO |

#### Subtasks для каждого Nested Issue Detail

| № | Subtask | Endpoint | API Status |
|---|---------|----------|------------|
| X.1 | Reading progress (volume + parent) | /api/volumes/\<slug\>/, /api/\<parent\>/\<slug\>/ | Volume NEEDS WORK; varies |
| X.2 | Previous/Next (within sublist) | /api/\<parent\>/\<slug\>/issues/\<issue_slug\>/ | **PLAN** |

**Все 9 nested issue details требуют по 1 PLAN endpoint для prev/next.**

#### Сводка Phase 4.11-4.19

| Метрика | Значение |
|---------|----------|
| Задач | 9 |
| Сложность каждой | M |
| Backend PLAN | 9 endpoints (prev/next для каждого parent) |
| Блокируется NEEDS WORK | 6 (4.14-4.19) |
| Можно начать сразу | 3 (4.11, 4.12, 4.13) |

---

### Полная сводка Phase 4

| Подфаза | Задач | NEEDS WORK | PLAN | Сложность |
|---------|-------|------------|------|-----------|
| 4.1-4.4 Details (API готов) | 4 | 1 | 30 | 2×XL, 2×L |
| 4.5-4.10 Details (нужен backend) | 6 | 6 | 58 | 2×XL, 4×L |
| 4.11-4.19 Nested Issue Details | 9 | — | 9 | 9×M |
| **Итого Phase 4** | **19** | **7** | **97** | — |

---

## Phase 5: Search

**Backend работа:**
- `/api/search/` [PLAN] — поиск через django-watson
- `/api/search/ajax/` [PLAN] — autocomplete через django-watson

### 5.1 Search page [RC-162](https://nonameitem.atlassian.net/browse/RC-162) | Сложность: **L**

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 5.1.1 | Search form | /api/search/ | **PLAN** | [RC-162](https://nonameitem.atlassian.net/browse/RC-162) |
| 5.1.2 | Search results | /api/search/ | **PLAN** | [RC-162](https://nonameitem.atlassian.net/browse/RC-162) |
| 5.1.3 | AJAX autocomplete | /api/search/ajax/ | **PLAN** | [RC-267](https://nonameitem.atlassian.net/browse/RC-267) |

**Примечание:** Используется django-watson — нужно создать DRF view поверх существующего Watson search.

**Итого Phase 5:** 1 задача, 2 backend endpoints

---

## Phase 6: Missing Issues (Admin)

**Примечание:** Все страницы доступны только для staff.

### 6.1 Missing issues list [RC-23](https://nonameitem.atlassian.net/browse/RC-23) | Сложность: **XL**

**Блокер:** /api/missing-issues/ [NOT READY — no serializer_class]

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 6.1.1 | Issues table | /api/missing-issues/ | **NOT READY** | [RC-185](https://nonameitem.atlassian.net/browse/RC-185) |
| 6.1.2 | Purge deleted | /api/missing-issues/purge-deleted/ | **PLAN** | [RC-246](https://nonameitem.atlassian.net/browse/RC-246) |
| 6.1.3 | DO Reload modal | /api/missing-issues/reload-from-do/ | **PLAN** | [RC-247](https://nonameitem.atlassian.net/browse/RC-247) |
| 6.1.4 | Skip publisher | /api/missing-issues/skip-publisher/\<id\>/ | **PLAN** | [RC-248](https://nonameitem.atlassian.net/browse/RC-248) |
| 6.1.5 | Ignore publisher | /api/missing-issues/ignore-publisher/\<id\>/ | **PLAN** | [RC-249](https://nonameitem.atlassian.net/browse/RC-249) |
| 6.1.6 | Skip volume | /api/missing-issues/skip-volume/\<id\>/ | **PLAN** | [RC-250](https://nonameitem.atlassian.net/browse/RC-250) |
| 6.1.7 | Ignore volume | /api/missing-issues/ignore-volume/\<id\>/ | **PLAN** | [RC-251](https://nonameitem.atlassian.net/browse/RC-251) |
| 6.1.8 | Skip issue | /api/missing-issues/skip-issue/\<id\>/ | **PLAN** | [RC-252](https://nonameitem.atlassian.net/browse/RC-252) |
| 6.1.9 | Ignore issue | /api/missing-issues/ignore-issue/\<id\>/ | **PLAN** | [RC-253](https://nonameitem.atlassian.net/browse/RC-253) |

**Backend: 1 NOT READY + 8 PLAN**

---

### 6.2-6.10 Entity-specific Missing Issues

| № | Задача | Сложность | Endpoint | API Status | Jira |
|---|--------|-----------|----------|------------|------|
| 6.2 | Character missing issues [RC-144](https://nonameitem.atlassian.net/browse/RC-144) | M | /api/characters/\<slug\>/missing-issues/ | **PLAN** | [RC-186](https://nonameitem.atlassian.net/browse/RC-186) |
| 6.3 | Concept missing issues [RC-145](https://nonameitem.atlassian.net/browse/RC-145) | M | /api/concepts/\<slug\>/missing-issues/ | **PLAN** | [RC-187](https://nonameitem.atlassian.net/browse/RC-187) |
| 6.4 | Location missing issues [RC-146](https://nonameitem.atlassian.net/browse/RC-146) | M | /api/locations/\<slug\>/missing-issues/ | **PLAN** | [RC-188](https://nonameitem.atlassian.net/browse/RC-188) |
| 6.5 | Object missing issues [RC-147](https://nonameitem.atlassian.net/browse/RC-147) | M | /api/objects/\<slug\>/missing-issues/ | **PLAN** | [RC-189](https://nonameitem.atlassian.net/browse/RC-189) |
| 6.6 | Person missing issues [RC-148](https://nonameitem.atlassian.net/browse/RC-148) | M | /api/people/\<slug\>/missing-issues/ | **PLAN** | [RC-190](https://nonameitem.atlassian.net/browse/RC-190) |
| 6.7 | Publisher missing issues [RC-149](https://nonameitem.atlassian.net/browse/RC-149) | M | /api/publishers/\<slug\>/missing-issues/ | **PLAN** | [RC-191](https://nonameitem.atlassian.net/browse/RC-191) |
| 6.8 | Story arc missing issues [RC-150](https://nonameitem.atlassian.net/browse/RC-150) | M | /api/story-arcs/\<slug\>/missing-issues/ | **PLAN** | [RC-192](https://nonameitem.atlassian.net/browse/RC-192) |
| 6.9 | Team missing issues [RC-151](https://nonameitem.atlassian.net/browse/RC-151) | M | /api/teams/\<slug\>/missing-issues/ | **PLAN** | [RC-193](https://nonameitem.atlassian.net/browse/RC-193) |
| 6.10 | Volume missing issues [RC-152](https://nonameitem.atlassian.net/browse/RC-152) | M | /api/volumes/\<slug\>/missing-issues/ | **PLAN** | [RC-194](https://nonameitem.atlassian.net/browse/RC-194) |

**Backend: 9 PLAN endpoints**

---

### 6.11-6.13 Ignored Lists

| № | Задача | Сложность | Зависимости | Jira |
|---|--------|-----------|-------------|------|
| 6.11 | Ignored issues list [RC-24](https://nonameitem.atlassian.net/browse/RC-24) | M | Backend: 2 PLAN | TODO |
| 6.12 | Ignored volumes list [RC-25](https://nonameitem.atlassian.net/browse/RC-25) | M | Backend: 2 PLAN | TODO |
| 6.13 | Ignored publishers list [RC-26](https://nonameitem.atlassian.net/browse/RC-26) | M | Backend: 2 PLAN | TODO |

#### Subtasks

| № | Subtask | Endpoint | API Status | Jira |
|---|---------|----------|------------|------|
| 6.11.1 | Ignored issues table | /api/missing-issues/ignored-issues/ | **PLAN** | [RC-195](https://nonameitem.atlassian.net/browse/RC-195) |
| 6.11.2 | Delete ignored issue | /api/missing-issues/ignored-issues/\<pk\>/delete/ | **PLAN** | [RC-254](https://nonameitem.atlassian.net/browse/RC-254) |
| 6.12.1 | Ignored volumes table | /api/missing-issues/ignored-volumes/ | **PLAN** | [RC-196](https://nonameitem.atlassian.net/browse/RC-196) |
| 6.12.2 | Delete ignored volume | /api/missing-issues/ignored-volumes/\<pk\>/delete/ | **PLAN** | [RC-255](https://nonameitem.atlassian.net/browse/RC-255) |
| 6.13.1 | Ignored publishers table | /api/missing-issues/ignored-publishers/ | **PLAN** | [RC-197](https://nonameitem.atlassian.net/browse/RC-197) |
| 6.13.2 | Delete ignored publisher | /api/missing-issues/ignored-publishers/\<pk\>/delete/ | **PLAN** | [RC-256](https://nonameitem.atlassian.net/browse/RC-256) |

**Backend: 6 PLAN endpoints**

---

### 6.14-6.15 Error Pages

| № | Задача | Сложность | Зависимости | Jira |
|---|--------|-----------|-------------|------|
| 6.14 | 500 Error page [RC-265](https://nonameitem.atlassian.net/browse/RC-265) | S | — | [RC-288](https://nonameitem.atlassian.net/browse/RC-288) |
| 6.15 | 404 Error page [RC-266](https://nonameitem.atlassian.net/browse/RC-266) | S | — | [RC-289](https://nonameitem.atlassian.net/browse/RC-289) |

**Backend: Нет (frontend only)**

---

### Сводка Phase 6

| Подфаза | Задач | NOT READY | PLAN | Сложность |
|---------|-------|-----------|------|-----------|
| 6.1 Main missing issues | 1 | 1 | 8 | XL |
| 6.2-6.10 Entity missing issues | 9 | — | 9 | 9×M |
| 6.11-6.13 Ignored lists | 3 | — | 6 | 3×M |
| 6.14-6.15 Error pages | 2 | — | — | 2×S |
| **Итого Phase 6** | **15** | **1** | **23** | — |

---

## Финальная сводка

### Общий обзор

| Phase | Название | Задач | Done | Todo | Backend работа |
|-------|----------|-------|------|------|----------------|
| 1 | Auth | 5 | 3 | 2 | — |
| 1.5 | User Profile | 1 | — | 1 | — |
| 2 | Home & Dashboard | 2 | — | 2 | 2 PLAN |
| 3 | Entity Lists | 12 | — | 12 | — |
| 4.1-4.4 | Details (API готов) | 4 | — | 4 | 1 NEEDS WORK, 30 PLAN |
| 4.5-4.10 | Details (нужен backend) | 6 | — | 6 | 6 NEEDS WORK, 58 PLAN |
| 4.11-4.19 | Nested Issue Details | 9 | — | 9 | 9 PLAN |
| 5 | Search | 1 | — | 1 | 2 PLAN |
| 6 | Missing Issues (Admin) | 15 | — | 15 | 1 NOT READY, 23 PLAN |
| **Итого** | — | **56** | **3** | **53** | **8 NEEDS WORK, 124 PLAN** |

---

### Backend работа — Сводка

| Категория | Количество | Описание |
|-----------|------------|----------|
| **NOT READY** | 1 | Missing issues serializer (6.1) |
| **NEEDS WORK** | 7 | Detail serializers + slug lookup (4.5-4.10) + Volume для Issue progress (4.3.2) |
| **PLAN** | 124 | Новые endpoints (nested, actions, search) |

---

### Рекомендуемый порядок выполнения

```
Phase 1: Auth (1.3-1.4)
    ↓
Phase 1.5: User Profile
    ↓
Phase 3: Entity Lists (3.1-3.12) ← все API готовы, можно параллелить
    ↓
Phase 2: Home (2.1-2.2 + backend endpoints)
    ↓
Phase 4.1-4.4: Character, Concept, Issue, Location details
    │
    ├─→ Backend: 4.10 Volume detail serializer + slug (блокирует 4.3.2)
    │
Phase 4.5-4.10: Object, Person, Publisher, Story Arc, Team, Volume details
    ↓
Phase 4.11-4.19: Nested Issue Details
    ↓
Phase 5: Search (5.1 + backend endpoints)
    ↓
Phase 6: Missing Issues (6.1-6.15 + backend endpoints)
```

---

### Критический путь (блокеры)

1. **4.10 Volume detail serializer** → блокирует 4.3.2 Issue reading progress → блокирует 4.11-4.19
2. **4.5-4.10 NEEDS WORK entities** → блокируют 6 detail pages → блокируют 4.14-4.19
3. **6.1.1 Missing issues serializer** → блокирует всю Phase 6

---

### Оценка объёма

| Тип работы | S | M | L | XL |
|------------|---|---|---|---|
| Frontend страницы | 19 | 23 | 9 | 6 |
| Backend endpoints | ~80 | ~30 | ~10 | ~4 |