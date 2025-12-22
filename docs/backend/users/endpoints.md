# Users API endpoints

The `read_comics.users.api.views` module exposes three authenticated profile-related endpoints under `/api/profile/` plus `change-email` and `finished-stats` helpers.

## `GET /api/profile/` (ProfileView)
- **Action**: `retrieve`
- **Permissions**: authenticated only.
- **Serializer**: `ProfileSerializer`.
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

## `PATCH/PUT /api/profile/`
- **Action**: `partial_update` / `update`
- **Allowed writable fields**: `name`, `images` (file upload or base64), `gender`, `bio`, `birth_date`.
- **Validation**: unknown fields trigger a validation error.
- **Example request**:
  ```json
  {
    "name": "Reader One Jr.",
    "bio": "Collects cosmic runs.",
    "gender": {"value": "M"}
  }
  ```
- **Response**: same shape as `GET /api/profile/` with updated values.

## `GET /api/profile/finished-stats/` (FinishedIssuesStatsView)
- **Action**: `get`
- **Permissions**: authenticated only.
- **Response**:
  ```json
  {
    "finished_count": 120,
    "today_finished_count": 2,
    "reading_speed": 3.5
  }
  ```

## `PUT/PATCH /api/profile/change-email/` (ChangeEmailView)
- **Serializer**: `ChangeEmailSerializer`.
- **Payload**:
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
- **Notes**: `verified` is read-only, and changing the address resets verification.

## Input payloads
All endpoints above require authentication and only allow the fields documented above; there are no anonymous write operations.

## `api/auth/` (dj-rest-auth)
The `api/auth/` namespace uses the defaults provided by `dj-rest-auth` to expose login, logout, password reset, and session/token management. These endpoints do not require the `ProfileView` serializer and are largely handled by the third-party package.

### `POST /api/auth/login/`
- **Payload**:
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
- Returns `400` if credentials are invalid.
- The endpoint accepts whichever identifier `ACCOUNT_AUTHENTICATION_METHOD` allows (currently `"username"`), but the frontend may pass email if your Allauth adapter accepts it.

### `POST /api/auth/logout/`
- **Action**: invalidates the current auth token/session.
- **Payload**: none.
- **Response**:
  ```json
  {
    "detail": "Successfully logged out."
  }
  ```

### `POST /api/auth/password/reset/`
- **Payload**:
  ```json
  {
    "email": "reader1@example.com"
  }
  ```
- Sends a password reset link to the email and returns `{"detail": "Password reset e-mail has been sent."}`.
- Uses `users.api.serializers.ResetPasswordSerializer` (`REST_AUTH["PASSWORD_RESET_SERIALIZER"]`), which simply delegates to dj-rest-auth; the serializer prevents creation/update operations since this flow only triggers email delivery.

### `POST /api/auth/password/reset/confirm/`
- **Payload** (from email link):
  ```json
  {
    "uid": "<uidb64>",
    "token": "<token>",
    "new_password1": "newpass",
    "new_password2": "newpass"
  }
  ```
- Returns `200` on success, `400` for invalid token/data.
- Because `ACCOUNT_LOGIN_ON_PASSWORD_RESET` is `True`, dj-rest-auth may automatically authenticate the user after a successful password reset.

### `POST /api/auth/token/refresh/`
- **Payload**:
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
- Returns `401` if the refresh token is expired/invalid.
- The endpoint matches `rest_framework_simplejwt`’s refresh view, so the `SIMPLE_JWT` lifetimes in `config/settings/base.py` (`ACCESS_TOKEN_LIFETIME`, `REFRESH_TOKEN_LIFETIME` and related rotation/blacklist flags) directly influence how often clients must rotate tokens.

## `api/auth/registration/`
`dj-rest-auth.registration` exposes registration-related flows.

### `POST /api/auth/registration/`
- **Payload**:
  ```json
  {
    "username": "reader1",
    "email": "reader1@example.com",
    "password1": "securepass",
    "password2": "securepass"
  }
  ```
- **Response**: newly created user representation from `dj-rest-auth` (including `key` if REST auth returns it) or serialized user data.
- Requires email confirmation if `ACCOUNT_EMAIL_VERIFICATION` is `mandatory`.
- Because `ACCOUNT_EMAIL_VERIFICATION` is set to `"optional"` in `config/settings/base.py`, new accounts receive a confirmation email but are allowed to log in before confirmation unless you override that variable.
- Registration availability follows `ACCOUNT_ALLOW_REGISTRATION` (from `DJANGO_ACCOUNT_ALLOW_REGISTRATION`); if that flag is `False`, `POST /api/auth/registration/` will return `403` even if the payload is valid.

### `GET /api/auth/registration/account-confirm-email/{key}/`
- **Description**: triggered by the confirmation link sent to the user; no JSON payload required.
- **Response**: HTML view or redirect handled by dj-rest-auth/Allauth; use frontend-confirmation flow.
- The redirect targets honor `ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL` / `ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL` from `config/settings/base.py`.

### `POST /api/auth/registration/resend-confirmation/`
- **Payload**:
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

The `api/auth/` and `api/auth/registration/` endpoints are provided directly by dj-rest-auth/Allauth; their exact behavior (email verification rules, required fields, social providers) is driven by the relevant toggles in `config/settings/base.py` (e.g., `ACCOUNT_EMAIL_VERIFICATION`, `ACCOUNT_AUTHENTICATION_METHOD`, `REST_AUTH_SERIALIZERS`). Refer to that settings file whenever you need to adjust how dj-rest-auth behaves.
