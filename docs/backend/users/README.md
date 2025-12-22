# Users

Provides the custom user model, authentication flows, and middleware integrations.

## Key modules
- `models.py`, `forms.py`, and `admin.py` define the `User` model, admin panels, and registration flows.
- `adapters.py` and `context_processors.py` integrate with `django-allauth` and expose user data to templates.
- `middleware.py` tracks user activity and ties the current request to the authenticated user.
- `api/` and `views.py` surface REST APIs for login, profile management, and account settings.
