# Users Model

## Summary

- `User` — Custom Django user model extending AbstractUser with profile data and reading progress tracking

## Reference

### User Model

Custom user model extending Django's AbstractUser. Adds profile information and reading progress properties.

#### Database Fields

**Inherited from AbstractUser:**

| Field Name | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Django primary key |
| `username` | CharField | Unique username for login |
| `email` | EmailField | Email address |
| `password` | CharField | Hashed password |
| `first_name` | CharField | First name |
| `last_name` | CharField | Last name |
| `is_active` | BooleanField | Account active status |
| `is_staff` | BooleanField | Staff/admin status |
| `is_superuser` | BooleanField | Superuser/administrator status |
| `date_joined` | DateTimeField | Account creation date |

**Custom Fields (defined in User model):**

| Field Name | Type | Description |
|---|---|---|
| `name` | CharField | Full name (max 255 chars) — auto-generated from first_name/last_name if not provided |
| `gender` | CharField | Gender choice (M/F/U/O, max 1 char, default=U/Unicorn) |
| `_user_image` | ThumbnailImageField | Profile image upload (nullable) — auto-generates thumbnails |
| `bio` | CharField | User biography (max 1000 chars, blank=True) |
| `birth_date` | DateField | Birth date (null=True, blank=True) |
| `show_email` | BooleanField | Whether to display email in profile (default=False) |
| `last_active` | DateTimeField | Last activity timestamp — updated by LastActiveMiddleware (null=True) |
| `unlimited_downloads` | BooleanField | Premium feature flag for unlimited downloads (default=False) |

#### Gender Choices

| Value | Label | Description |
|---|---|---|
| `M` | Male | Male |
| `F` | Female | Female |
| `U` | Unicorn | Prefer not to say / default choice |
| `O` | Other | Other |

#### Methods

| Method | Signature | Description |
|---|---|---|
| `__str__()` | `() → str` | Returns full `name` if set, otherwise title-cased `username` |
| `get_absolute_url()` | `() → str` | Returns URL for user detail view: `users:detail` with username kwarg |
| `save()` | `(decorated with @logging.logged) → None` | Auto-generates `name` field from `first_name`/`last_name` if `name` is blank |
| `get_started_and_not_finished()` | `(model: type[ModelTypeT]) → QuerySet[ModelTypeT]` | Generic method returning volumes/story-arcs user started but not finished |

#### Properties (Read-Only)

| Property | Return Type | Description |
|---|---|---|
| `image_url` | String (URL) | URL to user's profile image or default avatar based on gender |
| `image_thumb_url` | String (URL) | URL to thumbnail version (40x40) of profile image or default |
| `started_and_not_finished_volumes` | QuerySet[Volume] | Volumes user started reading but not completed (calls get_started_and_not_finished with Volume model) |
| `started_and_not_finished_story_arcs` | QuerySet[StoryArc] | Story arcs user started reading but not completed (calls get_started_and_not_finished with StoryArc model) |
| `email_verified` | Boolean | Whether user's primary email is verified (accesses django-allauth EmailAddress.verified) |
| `finished_count` | Integer | Total number of issues user has finished reading (counts Finished objects) |
| `today_finished_count` | Integer | Number of issues finished today (filters Finished by today's date) |
| `reading_speed` | Integer or None | Average issues per day across all finished issues (computed via annotate/aggregate on Finished) |

#### Relationships

| Relation | Type | Description |
|---|---|---|
| `emailaddress_set` | Reverse FK (from django-allauth) | Related EmailAddress objects for multi-email support and verification |
| `finished_issues` (type hint) | QuerySet[Issue] | Related Finished through-model objects tracking which issues user has read |

#### Model Meta

- **Django Configuration**: Set as `AUTH_USER_MODEL = "users.User"` in settings
- **Managers**: Uses default manager; querysets support reading progress filters
- **Related Name**: Various reverse relations from other models use custom related_names

## Details

### Profile Management

User-provided profile information:
- Gender for display preferences and default avatar selection
- Custom avatar image upload with automatic thumbnail generation
- Bio/biography text field (optional)
- Birth date (optional)
- Email visibility control (show_email flag)
- Full name (auto-generated or explicitly set)

### Reading Progress Tracking

System tracks through related `Finished` model (M2M through-model):
- **finished_count**: Total issues completed
- **today_finished_count**: Issues completed today
- **started_and_not_finished_volumes**: Volumes with at least 1 finished issue but not all
- **started_and_not_finished_story_arcs**: Story arcs with at least 1 finished issue but not all
- **reading_speed**: Average issues per day (computed from finish_date timestamps)

### LastActiveMiddleware Integration

Timestamp `last_active` tracks user activity:
- Updated by `LastActiveMiddleware` on each request
- Only updates if not set or older than `LAST_ACTIVE_TIMEOUT` setting
- Used for tracking active users and activity metrics
- Prevents excessive database writes via timeout threshold

### Email Verification via django-allauth

Uses django-allauth's EmailAddress model:
- Primary email tracked separately from User.email
- `email_verified` property checks primary EmailAddress.verified flag
- Multiple email addresses per user supported
- Verification via email token link

### Name Auto-Generation Logic

`save()` method auto-populates `name` field when blank:
1. If `name` is blank AND both `first_name` and `last_name` exist → combines them
2. Else if `name` is blank AND only `first_name` exists → uses `first_name`
3. Else if `name` is blank AND only `last_name` exists → uses `last_name`
4. Used in `__str__()` display method

Method decorated with `@logging.logged` for audit trail.

### Avatar Image Handling

Image handling via ThumbnailImageField:
- Upload destination: `user_image/{username}_logo.{extension}`
- Auto-generates 40x40 thumbnail from original
- `image_url` property returns original or default avatar `/static/images/avatars/{gender}.png`
- `image_thumb_url` property returns thumbnail or default `/static/images/avatars/{gender}_thumb.png`
- Default avatars by gender: M.png, F.png, U.png, O.png

### QuerySet Methods

`get_started_and_not_finished(model)` returns entity (Volume/StoryArc) that user:
1. Has finished at least 1 issue in
2. Has NOT finished all issues in
3. Filters using Django ORM Q objects and Count aggregation
4. Annotates with finished_count and max_finished_date
5. Ordered by most recent completion date (recency)

Used by properties to provide filtered querysets of user's in-progress reading.

## References

- [middleware.md](middleware.md) — LastActiveMiddleware for tracking activity timestamps
- [api/serializers.md](api/serializers.md) — User serialization for API responses
- [api/views.md](api/views.md) — Profile management and statistics views