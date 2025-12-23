# Users API Views

## Summary

- `ProfileView` — Retrieve/update authenticated user's own profile
- `FinishedIssuesStatsView` — Retrieve reading statistics for authenticated user
- `ChangeEmailView` — Update authenticated user's primary email address

## Reference

### ProfileView

View for authenticated users to retrieve and update their own profile.

#### Base Class

Extends `RetrieveUpdateAPIView` from Django REST Framework.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `queryset` | `User.objects.all()` | Query all users (filtered by get_object) |
| `serializer_class` | `ProfileSerializer` | Serializer for profile data |
| `permission_classes` | `(IsAuthenticated,)` | Requires authentication |

#### Behavior

- `get_object()` always returns `self.request.user` (current authenticated user)
- Prevents users from accessing other users' profiles
- Supports GET (retrieve) and PATCH/PUT (update) operations

#### Related Serializer

- [ProfileSerializer](serializers.md#profileserializer) — Editable personal fields, read-only account data

---

### FinishedIssuesStatsView

View for retrieving authenticated user's reading statistics.

#### Base Class

Extends `APIView` from Django REST Framework.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `permission_classes` | `(IsAuthenticated,)` | Requires authentication |

#### Behavior

- GET-only view (no POST/PATCH/PUT/DELETE)
- Retrieves reading statistics from User model properties
- Defensive check ensures user is not AnonymousUser

#### Statistics Returned

Via User model properties:
- `finished_count` — Total issues completed
- `today_finished_count` — Issues completed today
- `reading_speed` — Average issues per day (float/int)

#### Error Handling

Raises `NotAuthenticated` exception if user is AnonymousUser (defensive check).

---

### ChangeEmailView

View for authenticated users to change their primary email address.

#### Base Class

Extends `UpdateAPIView` from Django REST Framework.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `serializer_class` | `ChangeEmailSerializer` | Serializer for email data |
| `permission_classes` | `(IsAuthenticated,)` | Requires authentication |

#### Behavior

- `get_object()` retrieves user's primary EmailAddress from django-allauth
- Supports GET (retrieve current email) and PATCH/PUT (update email)
- Updates EmailAddress.verified to False on email change
- Triggers django-allauth email verification flow

#### Related Serializer

- [ChangeEmailSerializer](serializers.md#changeemailserializer) — Email and verification status

#### Side Effects

On email change:
1. EmailAddress record updated with new email
2. Verification flag reset to False
3. django-allauth sends verification email with token
4. User must verify new email before it becomes primary

#### Error Handling

Raises `NotAuthenticated` exception if user is AnonymousUser.

---

## View Configuration Summary

| View | Base Class | Operations | Auth Required |
|---|---|---|---|
| ProfileView | RetrieveUpdateAPIView | GET, PATCH, PUT | Yes |
| FinishedIssuesStatsView | APIView | GET | Yes |
| ChangeEmailView | UpdateAPIView | GET, PATCH, PUT | Yes |

## Details

### Self-Lookup Pattern

All three views use self-lookup instead of URL parameters:
- No need for user ID/username in URL
- `get_object()` always returns request.user
- Prevents accidental access to other users' data

### Type Checking

Both FinishedIssuesStatsView and ChangeEmailView perform:
```python
if isinstance(user, UserType):
```

Defensive check ensures user is actual User instance, not AnonymousUser.

### Email Verification Flow

After email change via ChangeEmailView:
1. django-allauth detects verified=False on EmailAddress
2. Sends verification email with token
3. User clicks link in email
4. EmailAddress.verified set to True
5. Email becomes primary/active

## References

- [auth.md](auth.md) — JWT authentication used by views
- [serializers.md](serializers.md) — ProfileSerializer and ChangeEmailSerializer
- [../models.md](../models.md) — User model with properties accessed by views
- [../middleware.md](../middleware.md) — LastActiveMiddleware tracking activity