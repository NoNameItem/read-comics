# Login Redirect Implementation Plan

## Overview
Реализация редиректа пользователя на исходную страницу после успешной аутентификации. Стандартный паттерн "return URL" - сохранение целевого URL в query-параметре `to` и редирект после логина.

## Current State Analysis
- **Login page**: `frontend/app/pages/users/login.vue` - базовая форма без обработки редиректа
- **User store**: `frontend/app/stores/user.js` - функция `login()` возвращает ошибку или undefined при успехе
- **UserMenu**: `frontend/app/components/UserMenu.vue` - кнопка логина с фиксированным `to="/users/login"`
- **Middleware**: отсутствует - нет защиты роутов и автоматического редиректа на логин
- **Reference implementation**: `frontend_old/middleware/02.auth.global.ts` и `frontend_old/pages/login.vue`

## Desired End State
1. При попытке доступа к защищённой странице неавторизованный пользователь перенаправляется на `/users/login?to=/original/path`
2. После успешного логина пользователь возвращается на исходную страницу (из `?to=`) или на главную (`/`)
3. При клике на "Log in" из любой страницы текущий путь сохраняется в query-параметре

## What We're NOT Doing
- Регистрация с редиректом (отдельная задача)
- Сброс пароля
- Email verification flow
- Защита конкретных страниц (нужно отдельно добавить `loginRequired: true` в meta)

## Implementation Approach
Используем стандартный Nuxt 3 паттерн:
1. Global middleware проверяет `meta.loginRequired` и редиректит на логин с `?to=`
2. Login page после успеха использует `router.replace(route.query.to || '/')`
3. UserMenu передаёт текущий путь при навигации на логин

---

## Phase 1: Auth Middleware

### Overview
Создание глобального middleware для защиты роутов, требующих авторизации.

### Changes Required:

#### 1. Create Auth Middleware
**File**: `frontend/app/middleware/auth.global.ts` (новый файл)

```typescript
export default defineNuxtRouteMiddleware((to, _from) => {
  const user = useUserStore()

  if (to.meta?.loginRequired && !user.loggedIn) {
    return navigateTo({
      path: '/users/login',
      query: { to: to.fullPath }
    })
  }
})
```

### Success Criteria:

#### Manual Verification:
- [x] Middleware создан и работает без ошибок при запуске приложения
- [x] Страницы без `loginRequired` доступны без авторизации
- [x] Готов к использованию (страницы с `loginRequired: true` будут редиректить)

---

## Phase 2: Login Page Update

### Overview
Добавление логики редиректа после успешного логина и обработки ошибок.

### Changes Required:

#### 1. Update Login Page
**File**: `frontend/app/pages/users/login.vue`

**Changes**:
- Добавить `useRoute`, `useRouter`, `useUserStore`
- Реализовать `onSubmit` с вызовом `userStore.login()`
- После успеха - `router.replace(route.query.to || '/')`
- Добавить отображение ошибок

```vue
<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'

definePageMeta({
  layout: 'blank'
})

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

const loading = ref(false)
const formError = ref<string | null>(null)

const fields: AuthFormField[] = [
  {
    name: 'login',
    type: 'string',
    label: 'Login',
    placeholder: 'Enter your login',
    required: true
  },
  {
    name: 'password',
    label: 'Password',
    type: 'password',
    placeholder: 'Enter your password',
    required: true
  }
]

const schema = z.object({
  login: z.string('Login is required').trim().min(1, 'Login is required'),
  password: z.string('Password is required').trim().min(1, 'Password is required')
})

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  loading.value = true
  formError.value = null

  const loginError = await userStore.login(payload.data.login, payload.data.password)

  if (loginError) {
    loading.value = false
    if (loginError?.response?.status === 400) {
      formError.value = loginError.response.data?.non_field_errors?.[0] || 'Invalid credentials'
    } else {
      formError.value = 'Network error. Please try again later.'
    }
    return
  }

  toast.add({
    title: `Welcome back, ${userStore.name || userStore.username}!`,
    color: 'success'
  })

  const redirectTo = route.query.to ? String(route.query.to) : '/'
  await router.replace(redirectTo)
}
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        :fields="fields"
        :loading="loading"
        title="Welcome back!"
        icon="i-lucide-lock"
        @submit="onSubmit"
      >
        <template #description>
          Don't have an account? <ULink to="#" class="text-primary font-medium">Sign up</ULink>.
        </template>
        <template #password-hint>
          <ULink to="#" class="text-primary font-medium" tabindex="-1">Forgot password?</ULink>
        </template>
        <template #validation>
          <UAlert v-if="formError" color="error" icon="i-lucide-circle-alert" :title="formError" />
        </template>
      </UAuthForm>
    </UPageCard>
  </div>
</template>
```

### Success Criteria:

#### Automated Verification:
- [x] Frontend type checking passes: `npm run typecheck`
- [x] Frontend linting passes: `npm run lint`

#### Manual Verification:
- [x] Успешный логин редиректит на `?to` или `/`
- [x] Неверные credentials показывают ошибку
- [x] Сетевые ошибки показывают соответствующее сообщение
- [x] Loading state отображается во время запроса

---

## Phase 3: UserMenu Update

### Overview
Передача текущего пути при переходе на страницу логина.

### Changes Required:

#### 1. Update UserMenu Component
**File**: `frontend/app/components/UserMenu.vue`

**Changes**:
- Добавить `useRoute()`
- Изменить `to` на объект с query-параметром

```vue
<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'

defineProps<{
  collapsed?: boolean
}>()

const route = useRoute()
const userStore = useUserStore()

// ... existing code ...
</script>

<template>
  <!-- ... existing dropdown ... -->
  <UButton
    v-else
    v-bind="{
      label: collapsed ? undefined : 'Log in',
      trailingIcon: collapsed ? undefined : 'i-lucide-log-in',
      leadingIcon: collapsed ? 'i-lucide-log-in' : undefined
    }"
    color="neutral"
    variant="ghost"
    block
    :square="collapsed"
    :ui="{
      trailingIcon: 'text-dimmed',
      leadingIcon: 'text-dimmed'
    }"
    :to="{ path: '/users/login', query: { to: route.fullPath } }"
  />
</template>
```

### Success Criteria:

#### Automated Verification:
- [x] Frontend type checking passes: `npm run typecheck`
- [x] Frontend linting passes: `npm run lint`

#### Manual Verification:
- [x] Клик на "Log in" с любой страницы сохраняет текущий путь в URL
- [x] После логина пользователь возвращается на исходную страницу

---

## Testing Strategy

### Manual Testing Steps:
1. Перейти на любую страницу (например `/characters`)
2. Нажать "Log in" в меню
3. Проверить что URL содержит `?to=/characters`
4. Ввести валидные credentials
5. Проверить редирект на `/characters`
6. Выйти и повторить с невалидными credentials - проверить ошибку
7. Проверить прямой переход на `/users/login` - редирект должен быть на `/`

### Edge Cases:
- Логин без `?to` параметра → редирект на `/`
- Невалидный `?to` (внешний URL) → проверить безопасность (опционально)
- Двойной логин (уже залогинен) → опционально добавить проверку

## Performance Considerations
Нет значительных performance implications - middleware выполняется синхронно.

## Migration Notes
Нет миграций данных. После деплоя функциональность сразу доступна.
