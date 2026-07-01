# Users Middleware

## Summary

- `LastActiveMiddleware` — Tracks last activity timestamp for authenticated users

## Reference

### LastActiveMiddleware

Django middleware that updates user's `last_active` timestamp on each request.

#### Configuration

Add to Django `MIDDLEWARE` setting:
```python
MIDDLEWARE = [
    # ... other middleware ...
    "read_comics.users.middleware.LastActiveMiddleware",
]
```

#### Behavior

Called on every request to:
1. Check if user is authenticated
2. Check if `last_active` timestamp needs update (based on `LAST_ACTIVE_TIMEOUT`)
3. Update `last_active` to current time if necessary
4. Save user model to database
5. Pass request to next middleware/view

#### Logic

```python
if user.is_authenticated:
    now = timezone.now()
    if (not user.last_active or
        now - user.last_active > timedelta(seconds=LAST_ACTIVE_TIMEOUT)):
        user.last_active = now
        user.save()
```

#### Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `LAST_ACTIVE_TIMEOUT` | Integer (seconds) | (required) | Minimum seconds between updates to avoid excessive saves |

#### Database Impact

- Minimal: Only saves to database when timeout has elapsed
- Example: If `LAST_ACTIVE_TIMEOUT = 3600` (1 hour), user.save() called max once per hour
- No updates for anonymous users (significantly reduces database load)

## Details

### Performance Optimization

The timeout prevents database churn:
- Without timeout: Would save on every single request (thousands/day per user)
- With timeout: Saves only when significant time has passed
- Example: 60 second timeout means max 1440 saves/user/day vs 86400+ without

### Use Cases

Track active users for:
- User presence/activity metrics
- Last activity display on profile
- Auto-logout or session cleanup based on inactivity
- Analytics and engagement tracking

### Limitations

- Doesn't track unauthenticated users (by design - performance)
- Doesn't track specific page/endpoint accessed
- Only updates once per timeout period (not real-time)
- Subject to database transaction timing

## References

- [models.md](models.md) — User model with last_active field
- [api/views.md](api/views.md) — Profile view returning last_active data