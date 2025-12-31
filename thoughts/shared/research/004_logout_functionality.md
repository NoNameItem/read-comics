---
date: 2025-12-30T12:00:00Z
researcher: Claude
topic: "Logout Functionality"
tags: [research, codebase, authentication, logout, jwt]
status: complete
---

# Research: How Logout Works

## Research Question
How does logout work in the ReadComics application?

## Summary

The logout functionality is **primarily client-side only**. The backend provides a logout endpoint via dj-rest-auth (`POST /api/auth/logout/`), but the frontend currently only clears local state without calling this endpoint. Additionally, the UserMenu "Log out" button is **not wired up** - clicking it does nothing.

## Detailed Findings

### Backend Logout (dj-rest-auth)

**Endpoint:** `POST /api/auth/logout/`

Provided by dj-rest-auth package, configured in:
- `config/urls.py:13` - URL routing
- `config/settings/base.py:377-382` - REST_AUTH configuration

**How it works:**
1. Accepts optional `{"refresh": "<token>"}` in request body
2. If refresh token provided, blacklists it in database
3. Returns `200 OK` with `{"detail": "Successfully logged out."}`

**Token Blacklisting Configuration:**

| Setting | Development | Production |
|---------|-------------|------------|
| BLACKLIST_AFTER_ROTATION | False | True |
| Blacklist App | Enabled | Enabled |

Files:
- `config/settings/base.py:387` - Dev: `BLACKLIST_AFTER_ROTATION: False`
- `config/settings/production.py:240` - Prod: `BLACKLIST_AFTER_ROTATION: True`

### Frontend Logout (Nuxt 3)

**Current Implementation:**

1. **Logout Function** (`frontend/app/stores/user.ts:148-150`):
   ```javascript
   const logout = () => {
     $reset()  // Clears all state including tokens
   }
   ```

2. **State Reset** (`frontend/app/stores/user.ts:45-59`):
   ```javascript
   const $reset = () => {
     accessToken.value = null
     refreshToken.value = null
     // ... clears all user data
   }
   ```

3. **Auto-Logout on 401** (`frontend/app/composables/useAxios.js:22-26`):
   ```javascript
   if (error.response?.status === 401 && originalRequest.url.includes('auth/token/refresh/')) {
     userStore.logout()
     userStore.$persist()
     return Promise.reject(error)
   }
   ```

**UserMenu Component** (`frontend/app/components/UserMenu.vue:33-38`):
```javascript
[
  {
    label: 'Log out',
    icon: 'i-lucide-log-out'
    // MISSING: onSelect handler to call logout
  }
]
```

### Data Flow

```
Current (Client-Side Only):
┌─────────────────────────────────────────────────────────┐
│ User clicks "Log out" (currently broken)                │
│              ↓                                          │
│     userStore.logout()                                  │
│              ↓                                          │
│     $reset() - clears all refs                          │
│              ↓                                          │
│     persist: true → localStorage cleared                │
│              ↓                                          │
│     loggedIn computed = false                           │
│              ↓                                          │
│     UI updates (shows login button)                     │
└─────────────────────────────────────────────────────────┘

Proper Implementation (Should Be):
┌─────────────────────────────────────────────────────────┐
│ User clicks "Log out"                                   │
│              ↓                                          │
│     POST /api/auth/logout/ with {refresh: token}        │
│              ↓                                          │
│     Backend blacklists refresh token                    │
│              ↓                                          │
│     userStore.logout()                                  │
│              ↓                                          │
│     Navigate to home/login page                         │
└─────────────────────────────────────────────────────────┘
```

## Code References

- `config/urls.py:13` - Auth URL routing (`path("api/auth/", include("dj_rest_auth.urls"))`)
- `config/settings/base.py:377-382` - REST_AUTH configuration
- `config/settings/base.py:383-388` - SIMPLE_JWT dev settings
- `config/settings/production.py:236-241` - SIMPLE_JWT prod settings
- `frontend/app/stores/user.ts:45-59` - `$reset()` function
- `frontend/app/stores/user.ts:148-150` - `logout()` function
- `frontend/app/composables/useAxios.js:22-26` - Auto-logout on refresh failure
- `frontend/app/components/UserMenu.vue:33-38` - Logout menu item (not wired up)
- `frontend/app/middleware/auth.global.ts:1-10` - Auth middleware (redirects after logout)

## Architecture Insights

1. **JWT Strategy:** Uses `dj-rest-auth` + `djangorestframework-simplejwt` with rotating refresh tokens
2. **Token Storage:** Frontend stores tokens in localStorage via Pinia persistence
3. **Blacklisting:** Only enabled in production; dev relies on token expiration
4. **Client-First Approach:** Frontend logout doesn't call backend - tokens remain valid server-side

## Issues Found

1. **UserMenu "Log out" button not functional** - Missing `onSelect` handler at `UserMenu.vue:35-37`
2. **No backend logout call** - Frontend only clears local state; refresh tokens remain valid until expiration
3. **No post-logout navigation** - User stays on current page after logout

## Security Considerations

1. **Token Validity:** If a refresh token is compromised, it remains valid for 60 days (dev) / 30 days (prod) even after "logout"
2. **Recommendation:** Frontend should call `POST /api/auth/logout/` with refresh token before clearing local state
3. **Production Mitigation:** `BLACKLIST_AFTER_ROTATION: True` limits attack window since each token refresh invalidates the old one

## Open Questions

None - the logout mechanism is clear, though incomplete in implementation.
