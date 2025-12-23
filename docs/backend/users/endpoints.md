# Users API endpoints

User endpoints are powered by custom API views (not viewsets) in `read_comics.users.api.views`. These include profile management, email changes, and authentication flows (via dj-rest-auth).

## Profile: `GET /api/profile/`

Retrieves the authenticated user's profile information including statistics and preferences.

- **View**: [`ProfileView`](views.md#profileview) (extends `RetrieveUpdateAPIView`)
- **Action**: `retrieve`
- **Serializer**: [`ProfileSerializer`](serializers.md#profileserializer)
- **Permissions**: `IsAuthenticated` only
- **Response fields**:
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

## Update Profile: `PATCH/PUT /api/profile/`

Updates the authenticated user's profile information. Supports partial updates via PATCH and full updates via PUT.

- **View**: [`ProfileView`](views.md#profileview) (extends `RetrieveUpdateAPIView`)
- **Action**: `partial_update` / `update`
- **Serializer**: [`ProfileSerializer`](serializers.md#profileserializer)
- **Permissions**: `IsAuthenticated` only
- **Writable fields**: `name`, `images` (file upload or base64), `gender`, `bio`, `birth_date`
- **Read-only fields**: `username`, `date_joined`, `email`, `email_verified`, `finished_count`, `reading_speed`
- **Request example**:
  ```json
  {
    "name": "Reader One Jr.",
    "bio": "Collects cosmic runs.",
    "gender": {"value": "M"}
  }
  ```
- **Response**: Same shape as `GET /api/profile/` with updated values
- **Validation**: Unknown fields trigger a validation error

## Finished Stats: `GET /api/profile/finished-stats/`

Returns reading statistics for the authenticated user, including total finished issues and reading speed.

- **View**: [`FinishedIssuesStatsView`](views.md#finishedissuesstatsview) (extends `APIView`)
- **Action**: `get`
- **Serializer**: None (returns plain JSON object)
- **Permissions**: `IsAuthenticated` only
- **Response**:
  ```json
  {
    "finished_count": 120,
    "today_finished_count": 2,
    "reading_speed": 3.5
  }
  ```

## Change Email: `PUT/PATCH /api/profile/change-email/`

Updates the authenticated user's email address and resets email verification status.

- **View**: [`ChangeEmailView`](views.md#changeemailview) (extends `UpdateAPIView`)
- **Action**: `update` / `partial_update`
- **Serializer**: [`ChangeEmailSerializer`](serializers.md#changeemailserializer)
- **Permissions**: `IsAuthenticated` only
- **Request payload**:
  ```json
  {
    "email": "new@example.com"
  }
  ```
- **Response**:
  ```json
  {
    "email": "new@example.com",
    "verified": false
  }
  ```
- **Note**: Changing the email address automatically resets `verified` to `false`, requiring re-confirmation

## Authentication endpoints (dj-rest-auth)

The `api/auth/` namespace uses the defaults provided by `dj-rest-auth` to expose login, logout, password reset, and session/token management. These endpoints are provided by the third-party package and configured via `config/settings/base.py`.

### Login: `POST /api/auth/login/`

Authenticates a user and returns JWT tokens.

- **Serializer**: Provided by dj-rest-auth (default login serializer)
- **Permissions**: Anonymous allowed
- **Request payload**:
  ```json
  {
    "email": "reader1@example.com",
    "password": "securepass"
  }
  ```
- **Response** (JWT per `REST_AUTH["USE_JWT"] = True`):
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJh...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhb..."
  }
  ```
- Returns `400` if credentials are invalid
- Accepts whichever identifier `ACCOUNT_AUTHENTICATION_METHOD` allows (currently `"username"`)

### Logout: `POST /api/auth/logout/`

Invalidates the current authentication token/session.

- **Serializer**: Provided by dj-rest-auth
- **Permissions**: `IsAuthenticated` only
- **Request payload**: None
- **Response**:
  ```json
  {
    "detail": "Successfully logged out."
  }
  ```

### Password Reset Request: `POST /api/auth/password/reset/`

Sends a password reset link to the user's email address.

- **Serializer**: [`ResetPasswordSerializer`](serializers.md#resetpasswordserializer) (custom, delegates to dj-rest-auth)
- **Permissions**: Anonymous allowed
- **Request payload**:
  ```json
  {
    "email": "reader1@example.com"
  }
  ```
- **Response**:
  ```json
  {
    "detail": "Password reset e-mail has been sent."
  }
  ```
- Uses custom URL generator to direct users to frontend password reset page

### Password Reset Confirm: `POST /api/auth/password/reset/confirm/`

Completes the password reset process using the token from the email link.

- **Serializer**: Provided by dj-rest-auth
- **Permissions**: Anonymous allowed
- **Request payload** (from email link):
  ```json
  {
    "uid": "<uidb64>",
    "token": "<token>",
    "new_password1": "newpass",
    "new_password2": "newpass"
  }
  ```
- Returns `200` on success, `400` for invalid token/data
- Because `ACCOUNT_LOGIN_ON_PASSWORD_RESET` is `True`, may automatically authenticate the user after successful reset

### Token Refresh: `POST /api/auth/token/refresh/`

Refreshes an access token using a valid refresh token.

- **Serializer**: Provided by `rest_framework_simplejwt`
- **Permissions**: Anonymous allowed (requires valid refresh token)
- **Request payload**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1Q..."
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJh..."
  }
  ```
- Returns `401` if the refresh token is expired/invalid
- Token lifetimes configured via `SIMPLE_JWT` settings (`ACCESS_TOKEN_LIFETIME`, `REFRESH_TOKEN_LIFETIME`)

## Registration endpoints (dj-rest-auth.registration)

The `api/auth/registration/` namespace exposes registration-related flows via dj-rest-auth.

### Register: `POST /api/auth/registration/`

Creates a new user account.

- **Serializer**: Provided by dj-rest-auth
- **Permissions**: Anonymous allowed (if `ACCOUNT_ALLOW_REGISTRATION` is `True`)
- **Request payload**:
  ```json
  {
    "username": "reader1",
    "email": "reader1@example.com",
    "password1": "securepass",
    "password2": "securepass"
  }
  ```
- **Response**: Newly created user representation from dj-rest-auth (including auth tokens if configured)
- Requires email confirmation if `ACCOUNT_EMAIL_VERIFICATION` is `mandatory`
- Because `ACCOUNT_EMAIL_VERIFICATION` is set to `"optional"`, new accounts receive a confirmation email but can log in before confirmation
- Returns `403` if `ACCOUNT_ALLOW_REGISTRATION` is `False`

### Confirm Email: `GET /api/auth/registration/account-confirm-email/{key}/`

Confirms a user's email address via the link sent during registration.

- **Serializer**: Provided by dj-rest-auth/Allauth
- **Permissions**: Anonymous allowed
- **Path parameter**: `{key}` (confirmation key from email)
- **Response**: HTML view or redirect handled by dj-rest-auth/Allauth
- Redirect targets honor `ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL` / `ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL`

### Resend Confirmation: `POST /api/auth/registration/resend-confirmation/`

Resends the email confirmation link to a user.

- **Serializer**: Provided by dj-rest-auth
- **Permissions**: Anonymous allowed
- **Request payload**:
  ```json
  {
    "email": "reader1@example.com"
  }
  ```
- **Response**:
  ```json
  {
    "detail": "Confirmation e-mail sent."
  }
  ```

## Notes

- All profile endpoints require authentication and only allow the fields documented above
- The `api/auth/` and `api/auth/registration/` endpoints are provided by dj-rest-auth/Allauth
- Exact behavior (email verification rules, required fields, social providers) is driven by settings in `config/settings/base.py`
- See `ACCOUNT_EMAIL_VERIFICATION`, `ACCOUNT_AUTHENTICATION_METHOD`, `REST_AUTH_SERIALIZERS`, and `SIMPLE_JWT` settings for configuration details