# Users API Authentication

## Summary

- `Auth` — Custom JWT cookie-based authentication class

## Reference

### Auth Class

Custom authentication class extending dj-rest-auth's JWTCookieAuthentication.

#### Configuration

```python
# In DRF settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "read_comics.users.api.auth.Auth",
        # ... other auth classes
    ],
}
```

#### Implementation

Extends `JWTCookieAuthentication` from dj-rest-auth package.

```python
class Auth(JWTCookieAuthentication):
    def authenticate(self, request):
        # Check if session exists before attempting JWT auth
        if not request.session.session_key:
            return None
        return super(Auth, self).authenticate(request)
```

#### Behavior

| Condition | Result |
|---|---|
| No session key present | Returns None (skips JWT auth) |
| Session key exists | Attempts JWT cookie authentication |
| JWT token valid | Returns (user, auth) tuple |
| JWT token invalid | Raises AuthenticationFailed |

#### Flow

1. Middleware initializes `request.session`
2. Auth class checks if session has been initialized (`session_key`)
3. If no session key, skips JWT authentication (returns None)
4. If session key exists, delegates to parent JWTCookieAuthentication
5. Parent class looks for JWT in cookies and validates

## Details

### Session-First Pattern

Custom logic enforces session initialization before JWT auth:
- Ensures session middleware has run first
- Prevents JWT-only attacks without valid session
- Allows fallback to session authentication if JWT not present
- Maintains session state alongside JWT tokens

### JWT Cookie Storage

Uses HTTP-only cookies (dj-rest-auth default):
- Token stored in cookie (not localStorage)
- Protected against XSS attacks
- Sent automatically with each request
- CSRF protection via tokens

### Django Session Integration

Works alongside Django's session framework:
- `request.session` initialized by SessionMiddleware
- Session state persists across requests
- Session variables accessible in views
- Supports session-based CSRF protection

## References

- [models.md](../models.md) — User model
- [serializers.md](serializers.md) — User serialization
- [views.md](views.md) — Authentication endpoints (login, logout)

## External References

- dj-rest-auth: JWT Cookie Authentication
- Django Sessions Framework
- SimpleJWT: JWT token handling