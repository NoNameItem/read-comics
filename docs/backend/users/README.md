# Users Module

Custom user model with authentication, profile management, and reading progress tracking.

## Documentation

- [models.md](models.md) — User model extending AbstractUser with profile and progress fields
- [middleware.md](middleware.md) — LastActiveMiddleware for tracking user activity
- [api/auth.md](api/auth.md) — JWT cookie authentication configuration
- [api/serializers.md](api/serializers.md) — User serializers for various API operations
- [api/views.md](api/views.md) — Profile, statistics, and email management views

## Key Features

- **Custom User Model**: Extends Django's AbstractUser with profile fields
- **Authentication**: JWT token-based with cookie storage (dj-rest-auth)
- **Profile Management**: Users can update name, bio, birth date, gender, avatar
- **Reading Progress**: Track finished issues, reading speed, in-progress content
- **Email Management**: Change primary email with verification flow (django-allauth)
- **Activity Tracking**: Last active timestamp updated via middleware

## User Model Fields

**Inherited from AbstractUser:**
- username, email, password, first_name, last_name
- is_active, is_staff, is_superuser, date_joined

**Custom Fields:**
- name, gender, bio, birth_date, _user_image
- show_email, last_active, unlimited_downloads

## Reading Progress Tracking

User properties:
- `finished_count` — Total issues completed
- `today_finished_count` — Issues completed today
- `reading_speed` — Average issues per day
- `started_and_not_finished_volumes` — In-progress volumes
- `started_and_not_finished_story_arcs` — In-progress story arcs

## Gender Choices

- M (Male)
- F (Female)
- U (Unicorn) — default/prefer not to say
- O (Other)

## API Operations

**Profile Management**
- Retrieve authenticated user's profile
- Update profile fields (name, bio, gender, birth_date, avatar)
- Read-only fields: username, email, date_joined, finished_count, reading_speed

**Reading Statistics**
- Retrieve finished_count, today_finished_count, reading_speed

**Email Management**
- View primary email address
- Change primary email (triggers verification)

## Authentication

- JWT tokens stored in HTTP-only cookies (via dj-rest-auth)
- Custom Auth class checks session before JWT auth
- Integration with django-allauth for email verification
- Multiple email addresses per user supported
