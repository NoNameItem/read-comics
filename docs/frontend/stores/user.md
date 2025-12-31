# User Store in `frontend/app/stores/user.ts`

Authentication, token management, and user profile state.

## Summary

- [`useUserStore`](#useuserstore) — main store export
- [State](#state) — reactive state properties
- [Computed](#computed) — derived properties
- [Actions](#actions) — store methods

## Reference

### useUserStore

Pinia store managing user authentication and profile.

**Options:**
- `persist: true` — state saved to localStorage

**Usage:**
```typescript
const userStore = useUserStore()
await userStore.login('username', 'password')
```

## State

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `accessToken` | `string \| null` | `null` | JWT access token |
| `refreshToken` | `string \| null` | `null` | JWT refresh token |
| `refreshingToken` | `boolean` | `false` | Token refresh in progress flag |
| `username` | `string \| null` | `null` | User's username |
| `name` | `string \| null` | `null` | User's display name |
| `email` | `string \| null` | `null` | User's email |
| `emailVerified` | `boolean \| null` | `null` | Email verification status |
| `gender` | `object \| null` | `null` | Gender with `value` property (M/F/O/U) |
| `images` | `object \| null` | `null` | Avatar images (`image`, `thumbnail`) |
| `birthDate` | `string \| null` | `null` | User's birth date |
| `registerDate` | `string \| null` | `null` | Registration date |
| `isSuperuser` | `boolean` | `false` | Superuser flag |
| `isStaff` | `boolean` | `false` | Staff flag |

## Computed

| Property | Type | Description |
|----------|------|-------------|
| `image` | `string` | User avatar or gender-based default |
| `thumbnail` | `string` | User thumbnail or gender-based default |
| `loggedIn` | `boolean` | `true` if `accessToken` is set |
| `isSuperuserOrStaff` | `boolean` | `true` if superuser or staff |
| `displayName` | `string` | `name` or `username` or empty string |

### Default Avatars

When user has no custom avatar, gender-based defaults are used:
- `F` — Female avatar
- `M` — Male avatar
- `O` — Other avatar
- `U` — Unknown/default avatar

## Actions

### login(username, password)

Authenticates user with credentials.

- **Parameters:**
  - `username`: `string` — username or email
  - `password`: `string` — user password
- **Returns:** `Error | undefined` — error object on failure, undefined on success
- **API Endpoint:** `POST /api/auth/login/`
- **Side Effects:** Sets tokens and user data on success

### register(username, email, password)

Registers new user account.

- **Parameters:**
  - `username`: `string` — desired username
  - `email`: `string` — user email
  - `password`: `string` — password (sent as `password1` and `password2`)
- **Returns:** `Error | undefined` — error object on failure
- **API Endpoint:** `POST /api/auth/registration/`
- **Side Effects:** Sets tokens and user data on success (status 201)

### logout()

Logs out user and blacklists refresh token.

- **Parameters:** none
- **Returns:** `Promise<void>`
- **API Endpoint:** `POST /api/auth/logout/`
- **Side Effects:**
  - Sends refresh token to backend for blacklisting
  - Calls `$reset()` to clear all state
  - Shows goodbye toast notification

### refreshTokens()

Refreshes JWT tokens using refresh token.

- **Parameters:** none
- **Returns:** `Promise<void>`
- **API Endpoint:** `POST /api/auth/token/refresh/`
- **Side Effects:** Updates `accessToken` and `refreshToken` on success

### setUser(user)

Updates user profile from API response.

- **Parameters:**
  - `user`: `object` — user data from API
- **Side Effects:** Updates all user-related state properties

### setTokens(accessToken, refreshToken)

Sets JWT tokens.

- **Parameters:**
  - `accessToken`: `string` — new access token
  - `refreshToken`: `string` — new refresh token

### setImage(user)

Updates user avatar images.

- **Parameters:**
  - `user`: `object` — object with `images` property

### resetImage()

Clears custom avatar, reverting to gender-based default.

### $reset()

Resets all state to initial values.

## Related

- [`useAxios`](../composables/useAxios.md) — HTTP client using this store for auth
- [`auth.global.ts`](../middleware/auth.global.md) — middleware checking `loggedIn`