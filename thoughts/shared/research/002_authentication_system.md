---
date: 2025-12-28T03:45:00+03:00
researcher: Claude
topic: "Как реализована аутентификация в системе?"
tags: [research, codebase, authentication, jwt, django, nuxt, security]
status: complete
---

# Research: Authentication System Implementation

## Research Question
Как реализована аутентификация в системе? (How is authentication implemented in the system?)

## Summary
ReadComics uses a **JWT-based authentication system** with a Django REST Framework backend and Nuxt 3 frontend. The implementation includes:

- **Backend**: Django + DRF with `djangorestframework-simplejwt` for JWT tokens, `dj-rest-auth` for authentication endpoints, and `django-allauth` for social authentication (Google, VK, Reddit, Discord)
- **Frontend**: Nuxt 3 with Pinia store for state management, axios interceptors for automatic token injection and refresh, and localStorage persistence
- **Token Strategy**: Short-lived access tokens (5-15 minutes), long-lived refresh tokens (30-60 days), automatic rotation with blacklisting in production
- **Security**: Argon2 password hashing, HTTPS enforcement in production, CORS protection, HSTS headers
- **Status**: Backend is fully implemented and tested; frontend has complete infrastructure but login page is **incomplete** (UI exists but doesn't call login function)

## Detailed Findings

### Backend Authentication Architecture

#### JWT Configuration
**Location**: `config/settings/base.py:371-388`, `config/settings/production.py:236-241`

The system uses three-tiered JWT configuration:

**Development Settings** (base.py):
```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  # Configurable via env
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),    # Configurable via env
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
}

REST_AUTH = {
    "USE_JWT": True,
    "USER_DETAILS_SERIALIZER": "read_comics.users.api.serializers.UserLoginSerializer",
    "PASSWORD_RESET_SERIALIZER": "read_comics.users.api.serializers.ResetPasswordSerializer",
    "JWT_AUTH_HTTPONLY": False,  # Tokens in response body, not cookies
}
```

**Production Overrides** (production.py:236-241):
- Access token: **5 minutes** (stricter)
- Refresh token: **30 days**
- Blacklisting: **Enabled** (old refresh tokens blacklisted after rotation)

**Key Architectural Decision**: Pure JWT authentication without session cookies for API. HTTP-only cookie mode is disabled, tokens are sent in response body and stored client-side.

#### Authentication Backends
**Location**: `config/settings/base.py:132-135`

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",           # Username/password
    "allauth.account.auth_backends.AuthenticationBackend",  # Social auth
]
```

Two backends enable both traditional username/password login and OAuth social authentication.

#### Middleware Stack
**Location**: `config/settings/base.py:164-184`

Authentication flow through middleware:
1. `CorsMiddleware` → Validates CORS headers for cross-origin requests
2. `SessionMiddleware` → Initializes session (needed for some auth flows)
3. `CsrfViewMiddleware` → CSRF protection
4. `AuthenticationMiddleware` → Populates `request.user` from JWT token
5. `AccountMiddleware` → Django-allauth session management
6. `LastActiveMiddleware` → Custom middleware tracking user activity

**Custom Middleware**: `read_comics/users/middleware.py:8-21`
```python
class LastActiveMiddleware:
    def __call__(self, request):
        user = request.user
        if user.is_authenticated and (
            not user.last_active
            or timezone.now() - user.last_active > timedelta(seconds=LAST_ACTIVE_TIMEOUT)
        ):
            user.last_active = timezone.now()
            user.save()
        return self.get_response(request)
```

Updates `user.last_active` field every 5 minutes (default timeout: 300s) to avoid database writes on every request.

#### Authentication Endpoints
**Location**: `config/urls.py:13-17, 37-39`

**dj-rest-auth endpoints** (`/api/auth/`):
- `POST /api/auth/login/` → Returns JWT access/refresh tokens and user data
- `POST /api/auth/logout/` → Invalidates current session
- `POST /api/auth/token/refresh/` → Refreshes access token
- `POST /api/auth/password/reset/` → Request password reset email
- `POST /api/auth/password/reset/confirm/` → Confirm password reset

**Registration endpoints** (`/api/auth/registration/`):
- `POST /api/auth/registration/` → Create new user account
- `POST /api/auth/registration/verify-email` → Confirm email address
- `POST /api/auth/registration/resend-email` → Resend confirmation email

**Custom profile endpoints** (`/api/profile/`):
- `GET/PATCH /api/profile/` → Get/update user profile
- `GET /api/profile/finished-stats/` → User reading statistics
- `PATCH /api/profile/change-email/` → Change user email

**Test Coverage**: All endpoints tested in `read_comics/users/tests/test_drf_urls.py:7-59`

### User Model and Permissions

#### Custom User Model
**Location**: `read_comics/users/models.py:29-120`
**Configuration**: `AUTH_USER_MODEL = "users.User"` (config/settings/base.py:137)

**Inheritance**: `User` → `AbstractUser` → `AbstractBaseUser` + `PermissionsMixin`

**Custom Fields**:
```python
# Profile
name = CharField(max_length=255, blank=True)  # Auto-generated from first/last
gender = CharField(max_length=1, choices=Gender.choices, default="U")
_user_image = ThumbnailImageField(null=True)
bio = CharField(max_length=1000, blank=True)
birth_date = DateField(null=True, blank=True)
show_email = BooleanField(default=False)

# Activity tracking
last_active = DateTimeField(null=True)

# Premium features
unlimited_downloads = BooleanField(default=False)
```

**Gender Choices**: M (Male), F (Female), U (Unicorn/prefer not to say), O (Other)

**Key Methods**:
- `save()` (models.py:68-77) → Auto-generates `name` from `first_name`/`last_name`
- `image_url` property (models.py:53-58) → Returns custom avatar or default by gender
- `finished_count` property (models.py:115-117) → Total issues finished by user
- `reading_speed` property (models.py:118-120) → Average issues per day

**Reading Progress Tracking** (models.py:79-113):
```python
def get_started_and_not_finished(self, model: type[ModelTypeT]) -> QuerySet[ModelTypeT]:
    """Returns volumes/story arcs the user started but hasn't finished"""
    return (
        model.objects.matched()
        .annotate(
            finished_count=Count("issues", filter=Q(issues__finished_users=self)),
            max_finished_date=Max("issues__finished__finish_date",
                                  filter=Q(issues__finished__user=self)),
        )
        .filter(finished_count__gte=1)
        .exclude(finished_count=F("issue_count"))
        .order_by("-max_finished_date")
    )
```

Generic method works for both volumes and story arcs, uses complex aggregation to track partial completion.

#### API Serializers
**Location**: `read_comics/users/api/serializers.py`

**UserLoginSerializer** (lines 25-42):
```python
fields = [
    "username", "name", "images", "email", "email_verified",
    "is_superuser", "is_staff", "gender", "birth_date", "date_joined",
]
```
Returns full user profile on login, used by `REST_AUTH.USER_DETAILS_SERIALIZER`.

**ProfileSerializer** (lines 66-92):
- Editable fields: `first_name`, `last_name`, `bio`, `birth_date`, `gender`, `show_email`, `_user_image`
- Read-only: `username`, `email`, `email_verified`, `finished_count`, `reading_speed`
- **Security feature**: Rejects unknown fields in `to_internal_value()` to prevent mass assignment vulnerabilities

**ResetPasswordSerializer** (lines 52-63):
```python
def password_reset_url_generator(request, user, temp_key) -> str:
    return (
        f"{settings.FRONTEND_BASE_URL}/password-reset-confirm"
        f"?uid={user_pk_to_url_str(user)}&token={temp_key}&email={user.email}"
    )
```
Custom URL generator redirects password reset to Nuxt frontend (default: `http://localhost:3000`).

**ChangeEmailSerializer** (lines 94-114):
- Validates email uniqueness with custom error message
- Resets `verified=False` when email changes
- Triggers django-allauth email verification flow

#### API Views
**Location**: `read_comics/users/api/views.py`

**ProfileView** (lines 18-24):
```python
class ProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> UserType | AnonymousUser:
        return self.request.user  # Always returns current user
```

**FinishedIssuesStatsView** (lines 27-40):
Returns user reading statistics:
```json
{
  "finished_count": 245,
  "today_finished_count": 5,
  "reading_speed": 12.3
}
```

**ChangeEmailView** (lines 43-51):
- Updates primary `EmailAddress` object (django-allauth)
- Requires re-verification after change

#### Custom Permission Classes
**Location**: `read_comics/utils/api/permissions.py:7-9`

```python
class IsSuperuserOrStaff(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and (request.user.is_superuser or request.user.is_staff))
```

Used for admin-only actions like technical info endpoints.

### Frontend Authentication

#### User Store (Pinia)
**Location**: `frontend/app/stores/user.js`

**State** (lines 30-43):
```javascript
const accessToken = ref(null)       // JWT access token
const refreshToken = ref(null)      // JWT refresh token
const refreshingToken = ref(false)  // Mutex for refresh operations
const username = ref(null)
const name = ref(null)
const email = ref(null)
const emailVerified = ref(null)
const gender = ref(null)
const images = ref(null)
const birthDate = ref(null)
const registerDate = ref(null)
const isSuperuser = ref(false)
const isStaff = ref(false)
```

**Computed Properties** (lines 61-66):
- `loggedIn` → `!!accessToken.value`
- `isSuperuserOrStaff` → `isSuperuser || isStaff`
- `image`/`thumbnail` → Falls back to default avatar by gender

**Authentication Methods**:

1. **Login** (lines 94-109):
```javascript
const login = async (username, password) => {
  const axios = useAxios()
  const response = await axios.post('/auth/login/', { password, username })
  if (response?.status === 200) {
    const data = await response.data
    setTokens(data.access, data.refresh)
    setUser(data.user)
  }
}
```

2. **Token Refresh** (lines 111-123):
```javascript
const refreshTokens = async () => {
  const axios = useAxios()
  const response = await axios.post('/auth/token/refresh/', { refresh: refreshToken.value })
  if (response.status === 200) {
    setTokens(data.access, data.refresh)
  }
}
```

3. **Registration** (lines 125-146):
```javascript
const register = async (username, email, password) => {
  const response = await axios.post('/auth/registration/', {
    email,
    password1: password,
    password2: password,
    username
  })
  // Auto-login on success
}
```

4. **Logout** (lines 148-150):
```javascript
const logout = () => {
  $reset()  // Clears all state including tokens
}
```

**Persistence** (line 184):
```javascript
{ persist: true }  // Auto-save to localStorage via pinia-plugin-persistedstate
```

All state automatically saved to `localStorage` with key `"user"`. Rehydrated on app initialization.

#### Axios Configuration
**Location**: `frontend/app/composables/useAxios.js`

**Base Instance** (line 57):
```javascript
const axiosIns = axios.create({ baseURL: 'http://127.0.0.1:8000/api' })
```

**⚠️ Issue**: Hardcoded API URL. Should use environment variable:
```javascript
const runtimeConfig = useRuntimeConfig()
const axiosIns = axios.create({ baseURL: runtimeConfig.public.apiBase })
```

**Request Interceptor** (lines 4-13):
```javascript
const requestInterceptor = async (config) => {
  const userStore = useUserStore()
  userStore.$hydrate()  // Load from localStorage

  if (userStore.accessToken) {
    config.headers.Authorization = `Bearer ${userStore.accessToken}`
  }

  return config
}
```

Automatically injects JWT token into all requests.

**Response Error Interceptor** (lines 15-52):

Handles 401 (Unauthorized) errors with automatic token refresh:

1. **401 on refresh endpoint** → Logout user (refresh token expired)
2. **401 on other endpoint** → Attempt token refresh:
   - Set `refreshingToken = true` mutex
   - Call `userStore.refreshTokens()`
   - Retry original request with new token
3. **Concurrent requests during refresh** → Poll every 100ms until refresh completes

**Token Refresh Flow**:
```
Request → 401 → Check if refresh endpoint
             ↓ No
         Check mutex (refreshingToken)
             ↓ false
         Set mutex, refresh tokens
             ↓
         Retry original request
             ↓ 401 again on another request
         Check mutex (refreshingToken)
             ↓ true (refresh in progress)
         Poll every 100ms until mutex clears
             ↓
         Retry when tokens refreshed
```

**⚠️ Issue**: Polling mechanism (lines 39-47) could create many interval timers. Better approach: Promise-based queue.

#### Login Page
**Location**: `frontend/app/pages/users/login.vue`

**Layout** (lines 5-7):
```javascript
definePageMeta({
  layout: 'blank'  // No sidebar/navigation
})
```

**Form Fields** (lines 11-26):
- `login` (text input)
- `password` (password input)

**Validation Schema** (lines 28-31):
```javascript
const schema = z.object({
  login: z.string().min(1, 'Login is required'),
  password: z.string().min(1, 'Password is required')
})
```

**⚠️ INCOMPLETE IMPLEMENTATION** (lines 35-37):
```javascript
function onSubmit(payload: FormSubmitEvent<Schema>) {
  console.log('Submitted', payload)  // Only logs, doesn't call login!
}
```

**Should be**:
```javascript
async function onSubmit(payload: FormSubmitEvent<Schema>) {
  const error = await userStore.login(payload.data.login, payload.data.password)
  if (!error) {
    router.push('/')
  } else {
    // Show error toast
  }
}
```

#### User Menu Component
**Location**: `frontend/app/components/UserMenu.vue`

**Logged In State** (line 43):
```vue
<UDropdown v-if="userStore.loggedIn" ... >
```

Shows user dropdown with profile options.

**Logged Out State** (lines 76-92):
```vue
<UButton label="Log in" to="/users/login" ... />
```

**⚠️ Issue**: Logout option in dropdown (lines 33-36) has no click handler:
```javascript
{
  label: 'Log out',
  icon: 'i-lucide-log-out',
  // Missing: onSelect: () => userStore.logout()
}
```

### Security Configuration

#### Password Hashing
**Location**: `config/settings/base.py:146-152`

```python
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",  # Primary (strongest)
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
```

Uses **Argon2** by default - industry best practice, winner of Password Hashing Competition.

**Test Override** (`config/settings/test.py:20`): Uses MD5 for speed during tests.

#### HTTPS and Security Headers (Production)
**Location**: `config/settings/production.py:40-57`

```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True                          # Force HTTPS
SESSION_COOKIE_SECURE = True                        # HTTPS-only cookies
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 518400                        # 6 days HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

Production enforces:
- HTTPS redirection
- HTTP Strict Transport Security (HSTS)
- Secure cookies
- Content-Type nosniff protection

#### CORS Configuration
**Location**: `config/settings/base.py:391-393`, `config/settings/production.py:243`

```python
# Base (development)
CORS_URLS_REGEX = r"^/api/.*$"  # Only API endpoints
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["*"])

# Production
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")  # Must be explicit
```

Development allows all origins (`["*"]`), production requires explicit whitelist.

#### Django-allauth Configuration
**Location**: `config/settings/base.py:327-366`

```python
ACCOUNT_AUTHENTICATION_METHOD = "username"  # Login by username, not email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"     # Can login before verifying
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True      # Auto-login after reset
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False   # Don't logout on password change
```

**Social Providers** (lines 84-88, 359-366):
- **Google**: Scope `["profile", "email"]`, online access
- **VK**: Default configuration
- **Reddit**: Permanent token, identity scope, custom user agent
- **Discord**: Default configuration

### Authentication Data Flow

#### Complete Authentication Flow

```
┌─────────────────────────────────────────┐
│ 1. User submits login form              │
│    frontend/app/pages/users/login.vue   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. userStore.login(username, password)  │
│    frontend/app/stores/user.js:94       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 3. Axios request interceptor            │
│    useAxios.js:4-13                      │
│    - Hydrate store from localStorage    │
│    - Add Authorization header            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 4. POST /api/auth/login/                │
│    dj-rest-auth → django-allauth         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 5. Middleware stack processing          │
│    - CorsMiddleware validates origin    │
│    - AuthenticationMiddleware validates │
│    - LastActiveMiddleware tracks time   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 6. SimpleJWT generates tokens           │
│    - Access token (15 min dev / 5 prod) │
│    - Refresh token (60 days / 30 prod)  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 7. UserLoginSerializer formats response │
│    serializers.py:25-42                  │
│    { access, refresh, user: {...} }     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 8. Frontend stores tokens & user data   │
│    - setTokens(access, refresh)         │
│    - setUser(userData)                  │
│    - Auto-persisted to localStorage     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 9. UI updates                           │
│    - userStore.loggedIn = true          │
│    - UserMenu shows dropdown            │
└─────────────────────────────────────────┘
```

#### Token Refresh Flow

```
┌─────────────────────────────────────────┐
│ API request with expired access token   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Backend returns 401 Unauthorized        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Response error interceptor              │
│ useAxios.js:15-52                        │
│ - Check if /auth/token/refresh/ ?      │
│   YES → Logout (refresh expired)        │
│   NO  → Attempt refresh                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Check refreshingToken mutex             │
│ - true  → Poll every 100ms              │
│ - false → Start refresh process         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ POST /api/auth/token/refresh/           │
│ Body: { refresh: refreshToken }         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ SimpleJWT validates & generates         │
│ - New access token                      │
│ - New refresh token (if rotation on)    │
│ - Blacklist old refresh (prod only)     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Update tokens in store                  │
│ Clear refreshingToken mutex             │
│ Retry original failed request           │
└─────────────────────────────────────────┘
```

## Code References

### Backend Core Files
- `config/settings/base.py:132-141` - Authentication backends and user model
- `config/settings/base.py:371-388` - REST_FRAMEWORK, REST_AUTH, SIMPLE_JWT configuration
- `config/settings/production.py:236-241` - Production JWT overrides
- `config/settings/production.py:40-57` - Production security settings
- `config/urls.py:13-17` - Authentication endpoint routing
- `config/urls.py:37-39` - Custom profile endpoints

### User Model
- `read_comics/users/models.py:29-120` - Custom User model
- `read_comics/users/models.py:68-77` - Auto name generation on save
- `read_comics/users/models.py:79-113` - Reading progress tracking methods
- `read_comics/users/middleware.py:8-21` - LastActiveMiddleware

### API Layer
- `read_comics/users/api/views.py:18-24` - ProfileView
- `read_comics/users/api/views.py:27-40` - FinishedIssuesStatsView
- `read_comics/users/api/views.py:43-51` - ChangeEmailView
- `read_comics/users/api/serializers.py:25-42` - UserLoginSerializer
- `read_comics/users/api/serializers.py:52-63` - ResetPasswordSerializer with custom URL generator
- `read_comics/users/api/serializers.py:66-92` - ProfileSerializer with over-posting protection
- `read_comics/users/api/serializers.py:94-114` - ChangeEmailSerializer
- `read_comics/utils/api/permissions.py:7-9` - IsSuperuserOrStaff permission

### Frontend Core Files
- `frontend/app/stores/user.js:30-43` - Authentication state
- `frontend/app/stores/user.js:94-109` - Login method
- `frontend/app/stores/user.js:111-123` - Token refresh method
- `frontend/app/stores/user.js:125-146` - Registration method
- `frontend/app/stores/user.js:148-150` - Logout method
- `frontend/app/stores/user.js:184` - Persistence configuration
- `frontend/app/composables/useAxios.js:4-13` - Request interceptor (token injection)
- `frontend/app/composables/useAxios.js:15-52` - Response error interceptor (auto-refresh)
- `frontend/app/composables/useAxios.js:57` - Axios instance creation (hardcoded URL)
- `frontend/app/pages/users/login.vue:35-37` - **INCOMPLETE**: Login form submission
- `frontend/app/components/UserMenu.vue:43` - Logged in state check
- `frontend/app/components/UserMenu.vue:33-36` - Logout menu item (no handler)

### Tests
- `read_comics/users/tests/test_drf_urls.py:7-59` - Authentication endpoint tests
- `read_comics/users/tests/factories.py:10-28` - UserFactory, SuperuserFactory

### Documentation
- `docs/backend/users/endpoints.md:5-249` - Complete endpoint documentation
- `docs/backend/users/models.md` - User model documentation
- `docs/backend/users/README.md` - Users module overview
- `docs/backend/users/api/README.md` - Users API overview

## Architecture Insights

### Design Patterns

1. **Layered Authentication**:
   - `dj-rest-auth` provides standard endpoints (`/api/auth/*`)
   - `rest_framework_simplejwt` handles token generation/validation
   - `django-allauth` provides social authentication backends
   - Custom views in `users/api/views.py` provide profile management

2. **Token Rotation Strategy**:
   - All environments: Rotation enabled
   - Development: Old refresh tokens remain valid (easier debugging)
   - Production: Old refresh tokens blacklisted (strict security)

3. **Frontend State Persistence**:
   - Pinia store with `pinia-plugin-persistedstate`
   - Entire auth state saved to localStorage
   - Manual `$hydrate()` calls ensure latest state in interceptors

4. **Automatic Token Refresh**:
   - Transparent to application code
   - Axios interceptor handles all 401 responses
   - Mutex prevents concurrent refresh requests
   - Failed requests automatically retried after refresh

5. **Activity Tracking**:
   - Custom middleware updates `last_active` timestamp
   - Rate-limited to once per 5 minutes (configurable)
   - Prevents excessive database writes

### Architectural Strengths

- ✅ **Industry-standard JWT implementation** with mature libraries
- ✅ **Short-lived access tokens** (5 minutes production) minimize risk
- ✅ **Token rotation** prevents replay attacks
- ✅ **Automatic token refresh** provides seamless UX
- ✅ **Multi-provider social auth** via django-allauth
- ✅ **Argon2 password hashing** (strongest available)
- ✅ **Comprehensive test coverage** for all endpoints
- ✅ **HTTPS enforcement** and HSTS in production
- ✅ **CORS protection** with origin whitelisting

### Architectural Weaknesses

- ⚠️ **localStorage token storage** vulnerable to XSS (standard SPA approach, but consider httpOnly cookies)
- ⚠️ **No token expiration checking** - relies on 401 responses (could decode JWT and check `exp` proactively)
- ⚠️ **Polling-based concurrent refresh handling** - could use Promise queue instead
- ⚠️ **Hardcoded API URL** in frontend - should use environment variables
- ⚠️ **No route guards/middleware** - frontend routes not protected (by design, most pages are public)
- ⚠️ **Silent error handling** in token refresh - empty catch block

### Technology Choices

**Why JWT over sessions?**
- ✅ Stateless - no server-side session storage needed
- ✅ Works across multiple domains (SPA + API separation)
- ✅ Mobile-friendly (no cookie support needed)
- ⚠️ Cannot invalidate tokens server-side (requires blacklist)
- ⚠️ Larger payload than session IDs

**Why dj-rest-auth?**
- ✅ Production-ready auth endpoints out of the box
- ✅ Seamless integration with django-allauth
- ✅ Customizable serializers and URL generators
- ✅ Well-maintained and widely used

**Why Pinia over Vuex?**
- ✅ Better TypeScript support
- ✅ Simpler API (no mutations)
- ✅ Built-in persistence plugin
- ✅ Official Vue 3 recommendation

## Answers to Open Questions

### Implementation Decisions (Confirmed with Team)

1. **Login page status**
   - ✅ **Work in progress** - Implementation will be completed as part of ongoing frontend development
   - UI form and validation are ready, just needs integration with `userStore.login()`

2. **Custom Auth class** (`read_comics/users/api/auth.py:5-9`)
   - ✅ **Obsolete code** - Can be safely removed
   - Not part of current architecture, not referenced in settings
   - No plans to require session + JWT combination

3. **httpOnly cookies vs localStorage**
   - ✅ **localStorage is sufficient** for this application
   - Application doesn't handle critical data requiring httpOnly cookie protection
   - Current security level (JWT in localStorage) is acceptable
   - No plans to migrate to httpOnly cookies

4. **Frontend auth middleware**
   - ✅ **Public access by design** - Most pages accessible to unauthenticated users
   - Auth protection will be added **per-page/per-component** as features are developed
   - No global auth middleware needed

5. **API URL configuration**
   - ✅ **Migration to env variables planned** in near future
   - Current hardcoded URLs (`http://127.0.0.1:8000/api`) are temporary
   - Will be replaced with `runtimeConfig.public.apiBase`

6. **Rate limiting for login attempts**
   - ✅ **Not required currently** - No immediate plans to implement
   - Expected user base is small (up to 5 authenticated users)
   - Can be added later if needed

7. **Token blacklist cleanup**
   - ✅ **Not a concern** - Expected user base is very small (up to 5 users)
   - Blacklist table growth is negligible with this scale
   - Automatic cleanup not needed at current scale

### Project Context

**Scale & Security Level:**
- Small user base (up to 5 authenticated users)
- Non-critical data (comic book reading progress, user preferences)
- Public read access for most content
- Authentication primarily for personalization features

**Development Approach:**
- Incremental feature development with per-feature auth decisions
- Security measures appropriate for scale and data sensitivity
- Focus on usability over maximum security hardening

### Future Considerations

1. **Mobile app support**
   - JWT architecture is mobile-friendly
   - Would need separate token storage (Keychain/Keystore)
   - Same backend endpoints could be reused

2. **Multi-factor authentication (MFA)**
   - No current plans
   - Django-allauth supports TOTP via `django-allauth-2fa` if needed
   - Would require additional endpoints and UI

3. **Enterprise features (if scale increases)**
   - Rate limiting (django-ratelimit)
   - Token blacklist cleanup jobs
   - Session management UI
   - MFA support
   - SSO integration (SAML, OAuth2)

## Recommendations

### Priority 1: Code Cleanup

1. **~~Remove obsolete Auth class~~** ✅ **COMPLETED**
   - ✅ Deleted `read_comics/users/api/auth.py` (unused `Auth(JWTCookieAuthentication)` class)
   - ✅ Deleted `docs/backend/users/api/auth.md` documentation
   - ✅ Removed all references from other documentation files
   - ✅ Updated authentication descriptions (localStorage instead of cookies)

### Priority 2: Planned Improvements (Near Future)

2. **Complete login page implementation** (frontend/app/pages/users/login.vue:35-37)
   - Currently WIP - just needs integration
   ```javascript
   async function onSubmit(payload: FormSubmitEvent<Schema>) {
     const error = await userStore.login(payload.data.login, payload.data.password)
     if (!error) {
       await router.push('/')
     } else {
       // Show error toast notification
     }
   }
   ```

3. **Add logout handler** (frontend/app/components/UserMenu.vue:33-36)
   ```javascript
   {
     label: 'Log out',
     icon: 'i-lucide-log-out',
     onSelect: () => {
       userStore.logout()
       router.push('/users/login')
     }
   }
   ```

4. **Migrate to environment-based API URL** (frontend/app/composables/useAxios.js:57)
   - Already planned for near future
   ```javascript
   // nuxt.config.ts
   runtimeConfig: {
     public: {
       apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000/api'
     }
   }

   // useAxios.js
   const config = useRuntimeConfig()
   const axiosIns = axios.create({ baseURL: config.public.apiBase })
   ```

### Priority 3: Quality Improvements

5. **Replace polling with Promise queue** in token refresh (useAxios.js:39-47)
   - Current: 100ms polling creates many interval timers
   - Better: Promise-based queue for concurrent refresh requests

6. **Add error handling UI**
   - Toast notifications for login failures
   - User-friendly error messages
   - Loading states during authentication

7. **Implement proactive token expiration checking**
   - Decode JWT and check `exp` claim before making requests
   - Preemptively refresh tokens before 401 errors
   - Reduces failed request retries

### Priority 4: Feature Completeness

8. **Create registration page** (frontend/app/pages/users/register.vue)
   - Use same `UAuthForm` pattern as login page
   - Integrate with `userStore.register()` method (already implemented)

9. **Add password reset flow**
   - Frontend pages for `/password-reset` and `/password-reset-confirm`
   - Backend already generates proper URLs redirecting to frontend

10. **Add auth protection to specific pages**
    - Not global middleware (most pages are public)
    - Per-page `definePageMeta({ middleware: 'auth' })` where needed
    - Component-level checks for sensitive actions

### Priority 5: Future Enhancements (If Scale Increases)

11. **Rate limiting** - django-ratelimit for login attempts
    - Not needed with current scale (5 users)
    - Consider if user base grows significantly

12. **Token blacklist cleanup job**
    - Celery task to purge expired blacklist entries
    - Not urgent with small user base

13. **Session management UI**
    - View active sessions/devices
    - Revoke specific sessions
    - Security feature for larger deployments

14. **Multi-factor authentication (MFA)**
    - TOTP support via django-allauth-2fa
    - Only if handling more sensitive data

15. **Implement token families**
    - Better multi-device support with rotation
    - Prevents token invalidation across devices
