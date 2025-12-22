# API permissions

## `IsSuperuserOrStaff`

- Simple permission class that allows access when `request.user` exists and either `is_superuser` or `is_staff` is true.
- Used by `TechnicalInfoActionMixin` so only privileged accounts can fetch internal metadata endpoints such as `/api/<resource>/<slug>/technical-info/`.
