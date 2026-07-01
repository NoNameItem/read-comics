# Users API Serializers

## Summary

- `UserSerializer` — Public user profile (minimal)
- `UserLoginSerializer` — Login response with full profile data
- `ProfileSerializer` — User's own profile (editable)
- `ResetPasswordSerializer` — Password reset request
- `ChangeEmailSerializer` — Email change management

## Reference

### UserSerializer

Public user profile serializer for displaying users in lists/detail views.

#### Fields

| Field Name | Type | Source | Description |
|---|---|---|---|
| `username` | CharField | Model | User's login username |
| `name` | CharField | Model | User's full name (computed or explicit) |
| `url` | HyperlinkedRelatedField | RO | Link to user detail endpoint |
| `image_thumb_url` | URLField | RO | Thumbnail image URL (40x40) |
| `last_active` | DateTimeField | Model | Last activity timestamp |

#### Meta Configuration

- **model**: User
- **fields**: 5 fields listed above (read-only except username/name)
- **extra_kwargs**: url field points to `api:user-detail` by username

---

### UserLoginSerializer

Returned after successful login with comprehensive user profile.

#### Fields

| Field Name | Type | Source | Description |
|---|---|---|---|
| `username` | CharField | Model | User's login username |
| `name` | CharField | Model | User's full name |
| `images` | ThumbnailImageField | Model | User's profile image with thumbnail |
| `email` | EmailField | Model | User's email address |
| `email_verified` | BooleanField | RO | Whether primary email is verified |
| `is_superuser` | BooleanField | Model | Whether user is superuser/admin |
| `is_staff` | BooleanField | Model | Whether user is staff member |
| `gender` | ChoiceField | Model | Gender choice (M/F/U/O) |
| `birth_date` | DateField | Model | User's birth date |
| `date_joined` | DateTimeField | Model | Account creation date |

#### Meta Configuration

- **model**: User
- **fields**: 10 fields listed above
- **Gender field**: Uses NestedChoiceField for User.Gender.choices

---

### ProfileSerializer

User's own profile (editable personal information).

#### Fields

| Field Name | Type | Writable | Description |
|---|---|---|---|
| `username` | CharField | No (RO) | User's login username |
| `name` | CharField | Yes | Full name (editable) |
| `images` | ThumbnailImageField | Yes | Profile image (editable, nullable) |
| `gender` | ChoiceField | Yes | Gender choice (editable) |
| `email` | EmailField | No (RO) | Primary email address |
| `email_verified` | BooleanField | No (RO) | Email verification status |
| `bio` | CharField | Yes | User biography (editable) |
| `finished_count` | Integer | No (RO) | Number of issues finished |
| `birth_date` | DateField | Yes | Birth date (editable) |
| `date_joined` | DateTimeField | No (RO) | Account creation timestamp |
| `reading_speed` | Float | No (RO) | Average issues per day |

#### Meta Configuration

- **model**: User
- **read_only_fields**: username, date_joined, email, email_verified, finished_count, reading_speed
- **Fields validation**: Custom `to_internal_value()` rejects unknown fields

#### Validation

Custom `to_internal_value()` method:
- Checks for unknown fields in input
- Raises ValidationError if extra fields provided
- Prevents over-posting of unexpected data

---

### ResetPasswordSerializer

Password reset request serializer (inherits from dj-rest-auth).

#### Behavior

- Extends dj-rest-auth's PasswordResetSerializer
- Overrides `get_email_options()` to customize reset email
- Uses custom URL generator for frontend password reset flow

#### Email Generation

```python
def password_reset_url_generator(request, user, temp_key) -> str:
    return (
        f"{FRONTEND_BASE_URL}/password-reset-confirm"
        f"?uid={user_pk_to_url_str(user)}&token={temp_key}&email={user.email}"
    )
```

- Generates reset link with uid, token, and email
- Points to frontend password reset page
- Uses `FRONTEND_BASE_URL` setting for cross-domain links

---

### ChangeEmailSerializer

Email change management serializer (works with EmailAddress model).

#### Fields

| Field Name | Type | Writable | Description |
|---|---|---|---|
| `email` | EmailField | Yes | New email address |
| `verified` | BooleanField | No (RO) | Verification status (always False on change) |

#### Meta Configuration

- **model**: EmailAddress (django-allauth)
- **fields**: email, verified
- **read_only_fields**: verified

#### Validation

Customizes UniqueValidator error message:
- Default: "User with this email address already exists"
- Applies to uniqueness check on email field

#### Update Logic

On email change:
1. Compares new email with current email
2. If different:
   - Updates email field
   - Sets `verified = False` (requires reverification)
   - Saves only updated fields to database
3. Returns updated EmailAddress instance

## Details

### Image Handling

- `images` field: ThumbnailImageField generates thumbnail automatically
- `image_thumb_url`: Property accessing 40x40 thumbnail
- Upload location: `user_image/{username}_logo.{ext}`
- Both source (_user_image) and thumb_url accessible

### Read-Only Fields Strategy

Different serializers expose different read-only fields:
- **UserSerializer**: Most fields read-only (public profile)
- **UserLoginSerializer**: All fields read-only (login response)
- **ProfileSerializer**: Editable personal fields, read-only account data
- **ChangeEmailSerializer**: Only email editable, verified read-only

### Password Reset Flow

1. User requests password reset with email
2. Django sends email with token and custom URL
3. Frontend navigates to `/password-reset-confirm?uid=...&token=...&email=...`
4. User submits new password
5. Backend validates token and updates password

### Email Verification

After email change:
- `verified` flag reset to False
- django-allauth sends verification email
- User must click link to verify new email
- Only verified emails become primary

## References

- [views.md](views.md) — API endpoints using these serializers
- [../models.md](../models.md) — User model definition