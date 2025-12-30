# Registration Page Implementation Plan

## Overview
Реализация страницы регистрации с поддержкой редиректа на исходную страницу после успешной регистрации. Аналогично login flow с `?to=` параметром.

## Current State Analysis
- **User store**: `frontend/app/stores/user.js:125-146` — функция `register(username, email, password)` готова
- **Login page**: `frontend/app/pages/users/login.vue` — образец для регистрации
- **Login link**: `frontend/app/pages/users/login.vue:82` — placeholder `to="#"` для Sign up
- **Backend**: `POST /api/auth/registration/` — готов (dj-rest-auth)
- **Email verification**: `ACCOUNT_EMAIL_VERIFICATION = "optional"` — нужно изменить на `"none"`

## Desired End State
1. Страница `/users/register` с формой регистрации (username, email, password, confirm password)
2. После успешной регистрации — редирект на `?to` или `/`
3. Ссылка "Sign up" на login page ведёт на `/users/register?to=...`
4. Email verification отключена

## What We're NOT Doing
- Email verification flow (verify-email, confirm-email pages)
- Social authentication
- Password strength indicator
- Terms of service checkbox

## Implementation Approach
Копируем структуру login.vue, адаптируем под регистрацию:
- 4 поля: username, email, password, confirm password
- Zod schema с валидацией совпадения паролей
- Вызов `userStore.register()` с одним паролем
- Toast + redirect после успеха

---

## Phase 1: Registration Page

### Overview
Создание страницы регистрации по образцу login.vue.

### Changes Required:

#### 1. Create Registration Page
**File**: `frontend/app/pages/users/register.vue` (новый файл)

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
    name: 'username',
    type: 'string',
    label: 'Username',
    placeholder: 'Enter your username',
    required: true
  },
  {
    name: 'email',
    type: 'string',
    label: 'Email',
    placeholder: 'Enter your email',
    required: true
  },
  {
    name: 'password',
    label: 'Password',
    type: 'password',
    placeholder: 'Enter your password',
    required: true
  },
  {
    name: 'confirmPassword',
    label: 'Confirm Password',
    type: 'password',
    placeholder: 'Confirm your password',
    required: true
  }
]

const schema = z
  .object({
    username: z.string().trim().min(1, 'Username is required'),
    email: z.string().trim().min(1, 'Email is required').email('Invalid email address'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
    confirmPassword: z.string().min(1, 'Please confirm your password')
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword']
  })

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  loading.value = true
  formError.value = null

  const registerError = await userStore.register(
    payload.data.username,
    payload.data.email,
    payload.data.password
  )

  if (registerError) {
    loading.value = false
    const axiosError = registerError as {
      response?: {
        status?: number
        data?: {
          username?: string[]
          email?: string[]
          password1?: string[]
          non_field_errors?: string[]
        }
      }
    }
    if (axiosError?.response?.status === 400) {
      const errors = axiosError.response.data
      formError.value =
        errors?.username?.[0] ||
        errors?.email?.[0] ||
        errors?.password1?.[0] ||
        errors?.non_field_errors?.[0] ||
        'Registration failed'
    } else {
      formError.value = 'Network error. Please try again later.'
    }
    return
  }

  toast.add({
    title: `Welcome, ${userStore.name || userStore.username}!`,
    color: 'success'
  })

  const redirectTo = route.query.to ? String(route.query.to) : '/'
  await router.replace(redirectTo)
}

const loginLink = computed(() => ({
  path: '/users/login',
  query: route.query.to ? { to: route.query.to } : undefined
}))
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        :fields="fields"
        :loading="loading"
        title="Create an account"
        icon="i-lucide-user-plus"
        submit-label="Sign up"
        @submit="onSubmit"
      >
        <template #description>
          Already have an account? <ULink :to="loginLink" class="text-primary font-medium">Log in</ULink>.
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
- [ ] Страница `/users/register` открывается
- [ ] Форма отображает 4 поля
- [ ] Валидация работает (пустые поля, несовпадение паролей, невалидный email)
- [ ] Успешная регистрация редиректит на `/`
- [ ] Ошибки бэкенда отображаются (username/email занят)

---

## Phase 2: Update Login Page Link

### Overview
Обновление ссылки "Sign up" на login page для перехода на регистрацию с сохранением `?to=`.

### Changes Required:

#### 1. Update Login Page
**File**: `frontend/app/pages/users/login.vue`

**Change**: Заменить placeholder ссылку на computed link с query параметром.

**Before** (line 82):
```vue
Don't have an account? <ULink to="#" class="text-primary font-medium">Sign up</ULink>.
```

**After**:
```vue
Don't have an account? <ULink :to="registerLink" class="text-primary font-medium">Sign up</ULink>.
```

**Add computed** (after line 15):
```typescript
const registerLink = computed(() => ({
  path: '/users/register',
  query: route.query.to ? { to: route.query.to } : undefined
}))
```

### Success Criteria:

#### Automated Verification:
- [x] Frontend type checking passes: `npm run typecheck`
- [x] Frontend linting passes: `npm run lint`

#### Manual Verification:
- [ ] Клик на "Sign up" с `/users/login` переходит на `/users/register`
- [ ] Клик на "Sign up" с `/users/login?to=/characters` переходит на `/users/register?to=/characters`

---

## Phase 3: Disable Email Verification

### Overview
Отключение email verification в настройках Django.

### Changes Required:

#### 1. Update Django Settings
**File**: `config/settings/base.py`

**Change**: Изменить `ACCOUNT_EMAIL_VERIFICATION` с `"optional"` на `"none"`.

**Before** (line 333):
```python
ACCOUNT_EMAIL_VERIFICATION = "optional"
```

**After**:
```python
ACCOUNT_EMAIL_VERIFICATION = "none"
```

### Success Criteria:

#### Manual Verification:
- [ ] После регистрации пользователь сразу залогинен
- [ ] Письмо с подтверждением email не отправляется

---

## Testing Strategy

### Manual Testing Steps:
1. Перейти на `/users/register`
2. Заполнить форму с валидными данными
3. Проверить успешную регистрацию и редирект на `/`
4. Выйти и повторить с `/characters` → login → Sign up → register → проверить редирект на `/characters`
5. Попробовать зарегистрировать существующий username — проверить ошибку
6. Попробовать зарегистрировать существующий email — проверить ошибку
7. Проверить валидацию несовпадения паролей

### Edge Cases:
- Короткий пароль (< 8 символов) — должна показаться ошибка
- Невалидный email — должна показаться ошибка
- Пустые поля — должна показаться ошибка

## Performance Considerations
Нет значительных performance implications.

## Migration Notes
Нет миграций данных. После деплоя функциональность сразу доступна.
