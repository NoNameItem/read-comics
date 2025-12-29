# Users API

REST API for user authentication, profile management, and reading statistics.

## Documentation

- [serializers.md](serializers.md) — User serializers (login, profile, email change, password reset)
- [views.md](views.md) — API views for profile, statistics, and email management

## Key Endpoints

| Purpose | View | Operations |
|---|---|---|
| User profile | ProfileView | GET, PATCH, PUT |
| Reading stats | FinishedIssuesStatsView | GET |
| Email change | ChangeEmailView | GET, PATCH, PUT |

Authentication required for all endpoints (JWT tokens via Authorization header).
