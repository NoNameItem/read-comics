---
date: 2025-12-30T12:00:00Z
researcher: Claude
topic: "Как устроена регистрация в системе"
tags: [research, codebase, registration, authentication, dj-rest-auth, allauth]
status: complete
---

# Research: Система регистрации пользователей

## Research Question
Как устроена регистрация в системе?

## Summary

Регистрация в системе реализована через стек **dj-rest-auth + django-allauth** на бэкенде. Кастомного кода для регистрации нет — используются стандартные view и serializer из библиотек. На фронтенде (Nuxt 3) страница регистрации **ещё не реализована**, но user store уже содержит функцию `register()`. В старом фронтенде (`frontend_old/`) есть полная реализация, которую можно использовать как референс.

## Detailed Findings

### Backend: API Registration

#### Endpoint
```
POST /api/auth/registration/
```

**URL route:** `config/urls.py:14`
```python
path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
```

#### Request Payload
```json
{
  "username": "string",
  "email": "string",
  "password1": "string",
  "password2": "string"
}
```

#### Success Response (201 Created)
```json
{
  "access": "JWT access token",
  "refresh": "JWT refresh token",
  "user": {
    "username": "...",
    "name": "...",
    "images": {"image": null, "thumbnail": null},
    "email": "...",
    "email_verified": false,
    "is_superuser": false,
    "is_staff": false,
    "gender": {"value": "U", "label": "Unicorn"},
    "birth_date": null,
    "date_joined": "..."
  }
}
```

#### Error Response (400 Bad Request)
```json
{
  "username": ["Пользователь с таким именем уже существует."],
  "email": ["Пользователь с таким Email уже существует."],
  "password1": ["Пароль слишком короткий."],
  "non_field_errors": ["Общие ошибки валидации"]
}
```

### Backend: Configuration

**File:** `config/settings/base.py:325-388`

| Setting | Value | Description |
|---------|-------|-------------|
| `ACCOUNT_ALLOW_REGISTRATION` | `env.bool(..., True)` | Можно отключить регистрацию |
| `ACCOUNT_AUTHENTICATION_METHOD` | `"username"` | Логин по username (не email) |
| `ACCOUNT_EMAIL_REQUIRED` | `True` | Email обязателен |
| `ACCOUNT_EMAIL_VERIFICATION` | `"optional"` | Верификация не блокирует логин |
| `REST_AUTH["USE_JWT"]` | `True` | Используются JWT токены |

### Backend: Custom Adapters

**File:** `read_comics/users/adapters.py`

**AccountAdapter (lines 12-31):**
- `is_open_for_signup()` — проверяет `ACCOUNT_ALLOW_REGISTRATION`
- `get_email_confirmation_url()` — генерирует URL для фронтенда: `{FRONTEND_BASE_URL}/confirm-email?key={key}`

### Backend: Data Flow

```
POST /api/auth/registration/
         ↓
dj_rest_auth.registration.views.RegisterView
         ↓
dj_rest_auth.registration.serializers.RegisterSerializer
         ↓
allauth.account.adapter.DefaultAccountAdapter (via custom AccountAdapter)
         ↓
User model created in PostgreSQL
         ↓
EmailAddress created (django-allauth)
         ↓
Verification email sent (если настроен email backend)
         ↓
JWT tokens generated (simplejwt)
         ↓
Response with tokens + UserLoginSerializer(user)
```

### Frontend: Current State

| Component | Новый фронтенд (`frontend/`) | Старый фронтенд (`frontend_old/`) |
|-----------|------------------------------|-----------------------------------|
| Registration page | **Отсутствует** | `frontend_old/pages/register.vue` |
| User store `register()` | `frontend/app/stores/user.js:125-146` | `frontend_old/stores/user.js:131-152` |
| Verify email page | **Отсутствует** | `frontend_old/pages/verify-email.vue` |
| Confirm email page | **Отсутствует** | `frontend_old/pages/confirm-email.vue` |

### Frontend: User Store Registration Function

**File:** `frontend/app/stores/user.js:125-146`

```javascript
const register = async (username, email, password) => {
  const axios = useAxios()
  const registerUrl = '/auth/registration/'

  try {
    const response = await axios.post(registerUrl, {
      email,
      password1: password,
      password2: password,
      username
    })

    if (response?.status === 201) {
      const data = await response.data
      setTokens(data.access, data.refresh)
      setUser(data.user)
    }
  } catch (e) {
    return e
  }
}
```

### Frontend: Login Page Placeholder

**File:** `frontend/app/pages/users/login.vue:82`
```vue
<ULink to="#" class="text-primary font-medium">Sign up</ULink>
```
Ссылка на регистрацию указывает на `#` — нужно обновить.

### Additional Registration Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/registration/` | POST | Создание пользователя |
| `/api/auth/registration/verify-email/` | POST | Подтверждение email по ключу |
| `/api/auth/registration/resend-email/` | POST | Повторная отправка письма |

## Code References

### Backend
- `config/urls.py:14` — URL route для регистрации
- `config/settings/base.py:325-388` — Конфигурация allauth и dj-rest-auth
- `read_comics/users/adapters.py:12-31` — Custom AccountAdapter
- `read_comics/users/api/serializers.py:25-42` — UserLoginSerializer (для response)
- `read_comics/users/models.py:29-119` — Custom User model

### Frontend (New)
- `frontend/app/stores/user.js:125-146` — Функция `register()`
- `frontend/app/pages/users/login.vue:82` — Placeholder ссылка на регистрацию

### Frontend (Old - Reference)
- `frontend_old/pages/register.vue` — Страница регистрации
- `frontend_old/pages/verify-email.vue` — Страница после регистрации
- `frontend_old/pages/confirm-email.vue` — Обработка email confirmation
- `frontend_old/composables/useResentEmailConfirmation.js` — Повторная отправка

## Architecture Insights

1. **Zero Custom Backend Code:** Регистрация полностью делегирована dj-rest-auth/allauth. Нет кастомных RegisterView или RegisterSerializer.

2. **JWT-first:** Система использует JWT токены (SimpleJWT), session auth только для DEBUG.

3. **Email Optional:** Email верификация настроена как `optional` — пользователь может пользоваться системой без подтверждения email.

4. **Frontend URL Generation:** AccountAdapter генерирует URL для фронтенда (не Django templates) для email confirmation.

5. **Consistent Error Format:** dj-rest-auth возвращает ошибки по полям (username, email, password1, non_field_errors).

## Open Questions

1. **Frontend Registration Page:** Нужна реализация `frontend/app/pages/users/register.vue` с использованием Nuxt UI (UAuthForm).

2. **Email Verification Flow:** Нужны страницы verify-email и confirm-email в новом фронтенде.

3. **Social Registration:** Есть конфигурация для Google, VK, Reddit, Discord — нужна ли поддержка на новом фронтенде?

4. **Registration Redirect:** После регистрации — редирект на verify-email или сразу на исходную страницу (как login)?
