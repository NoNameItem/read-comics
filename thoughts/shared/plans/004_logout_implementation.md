# Logout Implementation Plan

## Overview
Реализация полноценной функциональности logout: вызов backend API для инвалидации refresh token, toast-уведомление, подключение обработчика к кнопке в UI, умный редирект, и обработка автоматического logout при истечении refresh token.

## Current State Analysis

### Что есть:
- **Backend endpoint**: `POST /api/auth/logout/` (dj-rest-auth) - принимает `{"refresh": "<token>"}` для blacklist
- **User Store**: функция `logout()` в `stores/user.ts:148-150` - только очищает состояние
- **UserMenu**: кнопка "Log out" в `components/UserMenu.vue:33-38` - без обработчика
- **Auto-logout**: `composables/useAxios.js:22-26` - logout при 401 на refresh, без редиректа

### Что нужно:
1. Вызов backend API для инвалидации refresh token
2. Toast-уведомление "Bye, <name>. Hope to see you soon"
3. Подключение `onSelect` обработчика к dropdown item
4. Умный редирект после logout (в UserMenu и в interceptor)

## Desired End State

После нажатия "Log out" или автоматического logout:
1. Refresh token отправляется на backend и добавляется в blacklist
2. Toast: "Bye, <name>. Hope to see you soon"
3. Локальное состояние очищается (tokens, user data)
4. Пользователь перенаправляется:
   - Остаётся на текущей странице, если она не требует авторизации
   - Редирект на `/users/login?to=<path>`, если страница требует авторизацию или админские права

### Verification:
- [ ] Кнопка "Log out" в UserMenu работает
- [ ] Backend получает запрос с refresh token
- [ ] Toast-уведомление появляется с именем пользователя
- [ ] Состояние store очищается
- [ ] Редирект работает правильно для защищённых и публичных страниц
- [ ] Auto-logout в interceptor тоже показывает toast и делает редирект

## What We're NOT Doing
- Изменение backend logout endpoint (он уже работает)
- Изменение настроек token blacklisting

## Implementation Approach

Изменения в трёх файлах:
1. `stores/user.ts` - добавить вызов backend API и toast в `logout()`
2. `components/UserMenu.vue` - добавить `onSelect` с логикой редиректа
3. `composables/useAxios.js` - добавить редирект в `responseErrorInterceptor`

---

## Phase 1: Update User Store Logout Function

### Overview
Добавить вызов backend API и toast-уведомление в функцию `logout()`.

### Changes Required:

#### 1. User Store
**File**: `frontend/app/stores/user.ts`
**Changes**: Модифицировать функцию `logout()` для вызова backend API и показа toast

```javascript
// Заменить строки 148-150:
const logout = () => {
  $reset()
}

// На:
const logout = async () => {
  const axios = useAxios()
  const toast = useToast()

  // Сохраняем имя до $reset() для toast
  const userName = name.value || username.value

  // Отправляем refresh token на backend для blacklist
  // Игнорируем ошибки - logout должен работать даже если backend недоступен
  if (refreshToken.value) {
    try {
      await axios.post('/auth/logout/', { refresh: refreshToken.value })
    } catch (e) {
      // Игнорируем ошибки - очистка локального состояния важнее
    }
  }

  $reset()

  // Показываем toast после очистки состояния
  if (userName) {
    toast.add({
      title: `Bye, ${userName}. Hope to see you soon!`,
      color: 'success'
    })
  }
}
```

### Success Criteria:

#### Automated Verification:
- [x] Frontend type checking passes: `pnpm run typecheck`
- [x] Frontend linting passes: `pnpm run lint`

#### Manual Verification:
- [ ] При вызове `userStore.logout()` отправляется POST запрос на `/api/auth/logout/`
- [ ] Toast появляется с именем пользователя
- [ ] Состояние store очищается после вызова

---

## Phase 2: Wire Up UserMenu Logout Button

### Overview
Добавить `onSelect` обработчик к dropdown item "Log out" с логикой умного редиректа.

### Changes Required:

#### 1. UserMenu Component
**File**: `frontend/app/components/UserMenu.vue`
**Changes**: Добавить функцию logout и `onSelect` обработчик

Полный обновлённый `<script setup>`:

```vue
<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'

defineProps<{
  collapsed?: boolean
}>()

const route = useRoute()
const userStore = useUserStore()

const user = computed(() => ({
  name: userStore.name || '',
  avatar: {
    src: '~/assets/images/avatars/U_thumb.png',
    alt: userStore.name || ''
  }
}))

const handleLogout = async () => {
  // Проверяем, требует ли текущая страница авторизации или админских прав
  const requiresAuth = route.meta?.loginRequired
  const requiresAdmin = route.meta?.staffRequired || route.meta?.superuserRequired

  await userStore.logout()

  // Если страница требует авторизацию или админские права - редирект на login
  if (requiresAuth || requiresAdmin) {
    await navigateTo({
      path: '/users/login',
      query: { to: route.fullPath }
    })
  }
  // Иначе остаёмся на текущей странице
}

const items = computed<DropdownMenuItem[][]>(() => [
  [
    {
      type: 'label',
      label: user.value.name || '',
      avatar: user.value.avatar
    }
  ],
  [
    {
      label: 'Profile',
      icon: 'i-lucide-user'
    }
  ],
  [
    {
      label: 'Log out',
      icon: 'i-lucide-log-out',
      onSelect: handleLogout
    }
  ]
])
</script>
```

Template остаётся без изменений.

### Success Criteria:

#### Automated Verification:
- [x] Frontend formatting passes: `pnpm run format`
- [x] Frontend type checking passes: `pnpm run typecheck`
- [x] Frontend linting passes: `pnpm run lint`

#### Manual Verification:
- [ ] Клик на "Log out" в UserMenu вызывает logout
- [ ] Toast появляется с именем пользователя
- [ ] На публичной странице (/) - остаёмся после logout
- [ ] На странице с `loginRequired: true` - редирект на login с ?to=

---

## Phase 3: Add Redirect to Auto-Logout in Interceptor

### Overview
Добавить редирект при автоматическом logout (когда refresh token истёк и backend вернул 401).

### Changes Required:

#### 1. Axios Composable
**File**: `frontend/app/composables/useAxios.js`
**Changes**: Добавить редирект после logout в `responseErrorInterceptor`

```javascript
// Заменить строки 22-26:
if (error.response?.status === 401 && originalRequest.url.includes('auth/token/refresh/')) {
  userStore.logout()
  userStore.$persist()

  return Promise.reject(error)
}

// На:
if (error.response?.status === 401 && originalRequest.url.includes('auth/token/refresh/')) {
  await userStore.logout()
  userStore.$persist()

  // Редирект на login, если текущая страница требует авторизации
  const route = useRoute()
  const requiresAuth = route.meta?.loginRequired
  const requiresAdmin = route.meta?.staffRequired || route.meta?.superuserRequired

  if (requiresAuth || requiresAdmin) {
    await navigateTo({
      path: '/users/login',
      query: { to: route.fullPath }
    })
  }

  return Promise.reject(error)
}
```

### Success Criteria:

#### Automated Verification:
- [x] Frontend type checking passes: `pnpm run typecheck`
- [x] Frontend linting passes: `pnpm run lint`

#### Manual Verification:
- [ ] При истечении refresh token происходит автоматический logout
- [ ] Toast появляется
- [ ] Редирект происходит, если страница защищена

---

## Testing Strategy

### Manual Testing Steps:

1. **Тест ручного logout на публичной странице:**
   - Залогиниться
   - Перейти на главную страницу (/)
   - Нажать "Log out"
   - Ожидание: toast "Bye, <name>. Hope to see you soon!", остаёмся на главной

2. **Тест ручного logout на защищённой странице:**
   - Залогиниться
   - Перейти на страницу с `loginRequired` meta
   - Нажать "Log out"
   - Ожидание: toast + редирект на `/users/login?to=<путь>`

3. **Тест backend blacklist (DevTools):**
   - Залогиниться
   - Открыть Network tab
   - Нажать "Log out"
   - Ожидание: POST запрос на `/api/auth/logout/` с refresh token

4. **Тест при недоступном backend:**
   - Залогиниться
   - Остановить backend
   - Нажать "Log out"
   - Ожидание: logout и toast всё равно работают

5. **Тест автоматического logout:**
   - Залогиниться
   - Вручную изменить refresh token в localStorage на невалидный
   - Дождаться истечения access token (или изменить его тоже)
   - Сделать запрос к защищённому endpoint
   - Ожидание: auto-logout, toast, редирект если нужно

## Performance Considerations

Logout включает один дополнительный API запрос, но это критично для безопасности - инвалидация refresh token на сервере предотвращает использование украденных токенов.

## Migration Notes

Нет breaking changes. Существующий код, вызывающий `userStore.logout()`, будет работать (функция теперь async, но это backwards compatible).
