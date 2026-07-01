# Users API endpoints

User endpoints are powered by custom API views (not viewsets) in `read_comics.users.api.views`. These include profile management, email changes, and authentication flows (via dj-rest-auth).

## Profile: `GET /api/profile/`

Retrieves the authenticated user's profile information including statistics and preferences.

- **View**: [`ProfileView`](views.md#profileview) (extends `RetrieveUpdateAPIView`)
- **Action**: `retrieve`
- **Serializer**: [`ProfileSerializer`](serializers.md#profileserializer)
- **Permissions**: `IsAuthenticated` only

### Success Response

**`200 OK`**
```json
{
  "username": "reader1",
  "name": "Reader One",
  "images": {"image": "https://.../user.jpg", "thumbnail": "https://.../user_thumb.jpg"},
  "gender": {"value": "M", "label": "Male"},
  "email": "reader1@example.com",
  "email_verified": true,
  "bio": "Longtime fan of comics.",
  "finished_count": 120,
  "birth_date": "1990-01-01",
  "date_joined": "2020-05-15T12:00:00Z",
  "reading_speed": 3.5
}
```

### Error Responses

**`401 Unauthorized`** - No authentication credentials provided
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**`401 Unauthorized`** - Invalid or expired access token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

---

## Update Profile: `PATCH/PUT /api/profile/`

Updates the authenticated user's profile information. Supports partial updates via PATCH and full updates via PUT.

- **View**: [`ProfileView`](views.md#profileview) (extends `RetrieveUpdateAPIView`)
- **Action**: `partial_update` / `update`
- **Serializer**: [`ProfileSerializer`](serializers.md#profileserializer)
- **Permissions**: `IsAuthenticated` only
- **Writable fields**: `name`, `images` (file upload or base64), `gender`, `bio`, `birth_date`
- **Read-only fields**: `username`, `date_joined`, `email`, `email_verified`, `finished_count`, `reading_speed`

### Request Example
```json
{
  "name": "Reader One Jr.",
  "bio": "Collects cosmic runs.",
  "gender": {"value": "M"}
}
```

### Success Response

**`200 OK`** - Same shape as `GET /api/profile/` with updated values

### Error Responses

**`401 Unauthorized`** - No authentication credentials provided
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**`401 Unauthorized`** - Invalid or expired access token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

**`400 Bad Request`** - Unknown field in request body
```json
{
  "unknown_field_name": ["Unknown field."]
}
```

**`400 Bad Request`** - Invalid gender value
```json
{
  "gender": {
    "value": ["\"X\" is not a valid choice."]
  }
}
```

**`400 Bad Request`** - Invalid date format for birth_date
```json
{
  "birth_date": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."]
}
```

**`400 Bad Request`** - Name too long (max 255 chars)
```json
{
  "name": ["Ensure this field has no more than 255 characters."]
}
```

**`400 Bad Request`** - Bio too long (max 1000 chars)
```json
{
  "bio": ["Ensure this field has no more than 1000 characters."]
}
```

**`400 Bad Request`** - Invalid image format
```json
{
  "images": ["Upload a valid image. The file you uploaded was either not an image or a corrupted image."]
}
```

---

## Finished Stats: `GET /api/profile/finished-stats/`

Returns reading statistics for the authenticated user, including total finished issues and reading speed.

- **View**: [`FinishedIssuesStatsView`](views.md#finishedissuesstatsview) (extends `APIView`)
- **Action**: `get`
- **Serializer**: None (returns plain JSON object)
- **Permissions**: `IsAuthenticated` only

### Success Response

**`200 OK`**
```json
{
  "finished_count": 120,
  "today_finished_count": 2,
  "reading_speed": 3.5
}
```

### Error Responses

**`401 Unauthorized`** - No authentication credentials provided
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**`401 Unauthorized`** - Invalid or expired access token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

---

## Change Email: `PUT/PATCH /api/profile/change-email/`

Updates the authenticated user's email address and resets email verification status.

- **View**: [`ChangeEmailView`](views.md#changeemailview) (extends `UpdateAPIView`)
- **Action**: `update` / `partial_update`
- **Serializer**: [`ChangeEmailSerializer`](serializers.md#changeemailserializer)
- **Permissions**: `IsAuthenticated` only

### Request Payload
```json
{
  "email": "new@example.com"
}
```

### Success Response

**`200 OK`**
```json
{
  "email": "new@example.com",
  "verified": false
}
```
- **Note**: Changing the email address automatically resets `verified` to `false`, requiring re-confirmation

### Error Responses

**`401 Unauthorized`** - No authentication credentials provided
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**`401 Unauthorized`** - Invalid or expired access token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

**`400 Bad Request`** - Email already in use
```json
{
  "email": ["User with this e-mail address already exists."]
}
```

**`400 Bad Request`** - Invalid email format
```json
{
  "email": ["Enter a valid email address."]
}
```

**`400 Bad Request`** - Email field required
```json
{
  "email": ["This field is required."]
}
```

---

## Authentication endpoints (dj-rest-auth)

The `api/auth/` namespace uses the defaults provided by `dj-rest-auth` to expose login, logout, password reset, and session/token management. These endpoints are provided by the third-party package and configured via `config/settings/base.py`.

---

### Login: `POST /api/auth/login/`

Authenticates a user and returns JWT tokens.

- **Serializer**: Provided by dj-rest-auth (default login serializer)
- **Permissions**: Anonymous allowed
- **Authentication method**: `username` (configured via `ACCOUNT_AUTHENTICATION_METHOD`)

### Request Payload
```json
{
  "username": "reader1",
  "password": "securepass"
}
```

### Success Response

**`200 OK`** (JWT per `REST_AUTH["USE_JWT"] = True`)
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "username": "reader1",
    "name": "Reader One",
    "images": {"image": "https://.../user.jpg", "thumbnail": "https://.../user_thumb.jpg"},
    "email": "reader1@example.com",
    "email_verified": true,
    "is_superuser": false,
    "is_staff": false,
    "gender": {"value": "M", "label": "Male"},
    "birth_date": "1990-01-01",
    "date_joined": "2020-05-15T12:00:00Z"
  }
}
```

### Error Responses

**`400 Bad Request`** - Missing credentials
```json
{
  "username": ["This field is required."],
  "password": ["This field is required."]
}
```

**`400 Bad Request`** - Invalid credentials
```json
{
  "non_field_errors": ["Unable to log in with provided credentials."]
}
```

**`400 Bad Request`** - User account inactive
```json
{
  "non_field_errors": ["User account is disabled."]
}
```

---

### Logout: `POST /api/auth/logout/`

Invalidates the current authentication token/session.

- **Serializer**: Provided by dj-rest-auth
- **Permissions**: `IsAuthenticated` only
- **Request payload**: None (or optionally `{"refresh": "<token>"}` to blacklist refresh token)

### Success Response

**`200 OK`**
```json
{
  "detail": "Successfully logged out."
}
```

### Error Responses

**`401 Unauthorized`** - No authentication credentials provided
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**`401 Unauthorized`** - Invalid or expired access token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

---

### Password Reset Request: `POST /api/auth/password/reset/`

Sends a password reset link to the user's email address.

- **Serializer**: [`ResetPasswordSerializer`](serializers.md#resetpasswordserializer) (custom, delegates to dj-rest-auth)
- **Permissions**: Anonymous allowed
- **Note**: Uses custom URL generator to direct users to frontend password reset page

### Request Payload
```json
{
  "email": "reader1@example.com"
}
```

### Success Response

**`200 OK`**
```json
{
  "detail": "Password reset e-mail has been sent."
}
```
- **Note**: Returns success even if email doesn't exist (security measure to prevent email enumeration)

### Error Responses

**`400 Bad Request`** - Missing email field
```json
{
  "email": ["This field is required."]
}
```

**`400 Bad Request`** - Invalid email format
```json
{
  "email": ["Enter a valid email address."]
}
```

---

### Password Reset Confirm: `POST /api/auth/password/reset/confirm/`

Completes the password reset process using the token from the email link.

- **Serializer**: Provided by dj-rest-auth
- **Permissions**: Anonymous allowed
- **Note**: Because `ACCOUNT_LOGIN_ON_PASSWORD_RESET` is `True`, automatically authenticates the user after successful reset

### Request Payload (from email link)
```json
{
  "uid": "<uidb64>",
  "token": "<token>",
  "new_password1": "newpass",
  "new_password2": "newpass"
}
```

### Success Response

**`200 OK`**
```json
{
  "detail": "Password has been reset with the new password."
}
```

### Error Responses

**`400 Bad Request`** - Missing required fields
```json
{
  "uid": ["This field is required."],
  "token": ["This field is required."],
  "new_password1": ["This field is required."],
  "new_password2": ["This field is required."]
}
```

**`400 Bad Request`** - Invalid or expired token
```json
{
  "token": ["Invalid value"]
}
```

**`400 Bad Request`** - Invalid uid
```json
{
  "uid": ["Invalid value"]
}
```

**`400 Bad Request`** - Passwords don't match
```json
{
  "new_password2": ["The two password fields didn't match."]
}
```

**`400 Bad Request`** - Password too short (Django default: 8 chars minimum)
```json
{
  "new_password2": ["This password is too short. It must contain at least 8 characters."]
}
```

**`400 Bad Request`** - Password too common
```json
{
  "new_password2": ["This password is too common."]
}
```

**`400 Bad Request`** - Password entirely numeric
```json
{
  "new_password2": ["This password is entirely numeric."]
}
```

**`400 Bad Request`** - Password too similar to username
```json
{
  "new_password2": ["The password is too similar to the username."]
}
```

---

### Token Refresh: `POST /api/auth/token/refresh/`

Refreshes an access token using a valid refresh token.

- **Serializer**: Provided by `rest_framework_simplejwt`
- **Permissions**: Anonymous allowed (requires valid refresh token)
- **Token lifetimes**:
  - Access token: 15 minutes (configurable via `ACCESS_TOKEN_LIFETIME_MINUTES` env var)
  - Refresh token: 60 days (configurable via `REFRESH_TOKEN_LIFETIME_DAYS` env var)
- **Token rotation**: Enabled (`ROTATE_REFRESH_TOKENS = True`)

### Request Payload
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Success Response

**`200 OK`**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **Note**: New refresh token is returned because `ROTATE_REFRESH_TOKENS = True`

### Error Responses

**`401 Unauthorized`** - Missing refresh token
```json
{
  "detail": "No valid refresh token found.",
  "code": "token_not_valid"
}
```

**`401 Unauthorized`** - Expired refresh token
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

**`401 Unauthorized`** - Invalid refresh token
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

**`401 Unauthorized`** - Blacklisted refresh token
```json
{
  "detail": "Token is blacklisted",
  "code": "token_not_valid"
}
```

---

## Registration endpoints (dj-rest-auth.registration)

The `api/auth/registration/` namespace exposes registration-related flows via dj-rest-auth.

---

### Register: `POST /api/auth/registration/`

Creates a new user account.

- **Serializer**: Provided by dj-rest-auth
- **Permissions**: Anonymous allowed (if `ACCOUNT_ALLOW_REGISTRATION` is `True`)
- **Email verification**: Optional (`ACCOUNT_EMAIL_VERIFICATION = "optional"`)
  - New accounts receive a confirmation email but can log in before confirmation

### Request Payload
```json
{
  "username": "reader1",
  "email": "reader1@example.com",
  "password1": "securepass",
  "password2": "securepass"
}
```

### Success Response

**`201 Created`**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "username": "reader1",
    "name": "",
    "images": {"image": null, "thumbnail": null},
    "email": "reader1@example.com",
    "email_verified": false,
    "is_superuser": false,
    "is_staff": false,
    "gender": {"value": "U", "label": "Unicorn"},
    "birth_date": null,
    "date_joined": "2024-01-15T12:00:00Z"
  }
}
```

### Error Responses

**`403 Forbidden`** - Registration disabled
```json
{
  "detail": "You do not have permission to perform this action."
}
```
- Occurs when `ACCOUNT_ALLOW_REGISTRATION` is `False`

**`400 Bad Request`** - Missing required fields
```json
{
  "username": ["This field is required."],
  "email": ["This field is required."],
  "password1": ["This field is required."],
  "password2": ["This field is required."]
}
```

**`400 Bad Request`** - Username already taken
```json
{
  "username": ["A user with that username already exists."]
}
```

**`400 Bad Request`** - Email already registered
```json
{
  "email": ["A user is already registered with this e-mail address."]
}
```

**`400 Bad Request`** - Invalid email format
```json
{
  "email": ["Enter a valid email address."]
}
```

**`400 Bad Request`** - Passwords don't match
```json
{
  "non_field_errors": ["The two password fields didn't match."]
}
```

**`400 Bad Request`** - Password too short
```json
{
  "password1": ["This password is too short. It must contain at least 8 characters."]
}
```

**`400 Bad Request`** - Password too common
```json
{
  "password1": ["This password is too common."]
}
```

**`400 Bad Request`** - Password entirely numeric
```json
{
  "password1": ["This password is entirely numeric."]
}
```

**`400 Bad Request`** - Password too similar to username/email
```json
{
  "password1": ["The password is too similar to the username."]
}
```

**`400 Bad Request`** - Invalid username characters
```json
{
  "username": ["Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."]
}
```

---

### Confirm Email: `GET /api/auth/registration/account-confirm-email/{key}/`

Confirms a user's email address via the link sent during registration.

- **Serializer**: Provided by dj-rest-auth/Allauth
- **Permissions**: Anonymous allowed
- **Path parameter**: `{key}` (confirmation key from email)
- **Redirect targets**:
  - Anonymous users: `ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL` (`/`)
  - Authenticated users: `ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL` (`/`)
- **Auto-login**: `ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True`

### Success Response

**`302 Found`** - Redirects to configured URL after successful confirmation

### Error Responses

**`404 Not Found`** - Invalid or expired confirmation key
```json
{
  "detail": "Not found."
}
```

---

### Resend Confirmation: `POST /api/auth/registration/resend-confirmation/`

Resends the email confirmation link to a user.

- **Serializer**: Provided by dj-rest-auth
- **Permissions**: Anonymous allowed

### Request Payload
```json
{
  "email": "reader1@example.com"
}
```

### Success Response

**`200 OK`**
```json
{
  "detail": "ok"
}
```
- **Note**: Returns success even if email is already verified or doesn't exist (security measure)

### Error Responses

**`400 Bad Request`** - Missing email field
```json
{
  "email": ["This field is required."]
}
```

**`400 Bad Request`** - Invalid email format
```json
{
  "email": ["Enter a valid email address."]
}
```

---

## Common Error Responses

These error responses can occur on any endpoint:

### `405 Method Not Allowed`
Returned when using an unsupported HTTP method on an endpoint.
```json
{
  "detail": "Method \"DELETE\" not allowed."
}
```

### `415 Unsupported Media Type`
Returned when Content-Type header is incorrect or missing for POST/PUT/PATCH requests.
```json
{
  "detail": "Unsupported media type \"text/plain\" in request."
}
```

### `500 Internal Server Error`
Returned for unexpected server errors (details hidden in production).
```json
{
  "detail": "A server error occurred."
}
```

---

## Notes

- All profile endpoints require authentication and only allow the fields documented above
- The `api/auth/` and `api/auth/registration/` endpoints are provided by dj-rest-auth/Allauth
- Exact behavior (email verification rules, required fields, social providers) is driven by settings in `config/settings/base.py`
- See `ACCOUNT_EMAIL_VERIFICATION`, `ACCOUNT_AUTHENTICATION_METHOD`, `REST_AUTH_SERIALIZERS`, and `SIMPLE_JWT` settings for configuration details
- JWT tokens are stored in localStorage on the frontend and sent via `Authorization: Bearer <token>` header