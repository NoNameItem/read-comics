# useAxios in `frontend/app/composables/useAxios.js`

Configured Axios instance with JWT authentication interceptors.

## Summary

- [`useAxios`](#useaxios) — main composable export
- [Request Interceptor](#request-interceptor) — adds Authorization header
- [Response Interceptor](#response-interceptor) — handles 401 errors and token refresh

## Reference

### useAxios

Returns configured Axios instance for API requests.

**Returns:** `AxiosInstance` — configured Axios instance

**Configuration:**
- Base URL: `http://127.0.0.1:8000/api`
- Request interceptor: adds JWT token
- Response interceptor: handles 401 with token refresh

**Usage:**
```typescript
const axios = useAxios()
const response = await axios.get('/users/me/')
```

## Request Interceptor

Adds `Authorization: Bearer` header to all requests.

### Behavior

1. Calls `userStore.$hydrate()` to ensure latest state from localStorage
2. If `accessToken` exists, adds `Authorization: Bearer {token}` header
3. Returns modified config

## Response Interceptor

Handles 401 Unauthorized responses with automatic token refresh.

### Behavior

**Case 1: 401 on token refresh endpoint**
1. Calls `userStore.logout()` to clear state
2. Calls `userStore.$persist()` to save to localStorage
3. Checks if current route requires authentication (`loginRequired`, `staffRequired`, `superuserRequired`)
4. If protected route, redirects to `/users/login?to={currentPath}`
5. Rejects promise with original error

**Case 2: 401 on other endpoints (first attempt)**
1. Marks request as `_retry: true`
2. Hydrates user store state
3. If not already refreshing (`refreshingToken === false`):
   - Sets `refreshingToken = true`
   - Calls `userStore.refreshTokens()`
   - Sets `refreshingToken = false`
   - Retries original request with new token
4. If already refreshing:
   - Polls `refreshingToken` every 100ms
   - Retries request when refresh completes

**Case 3: Other errors**
- Rejects promise with original error

## Race Condition Prevention

The `refreshingToken` flag prevents multiple simultaneous token refresh requests:

1. First 401 response sets `refreshingToken = true`
2. Subsequent 401 responses wait via interval polling
3. After refresh completes, all waiting requests retry

## Related

- [`useUserStore`](../stores/user.md) — provides tokens and auth methods
- [`auth.global.ts`](../middleware/auth.global.md) — route protection middleware