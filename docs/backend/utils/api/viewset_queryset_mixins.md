# Viewset queryset mixins

These custom mixins decorate DRF viewsets to annotate counts, hide unfinished data, or limit fields before serialization.

## `OnlyWithIssuesQuerySetMixin`
- Hides objects with `issues_count == 0` unless `?show-all=yes` is passed.

## `ListOnlyQuerySetMixin`
- When viewing collections, limits the queryset to `list_only` fields to reduce memory pressure.

## `IssuesCountQuerySetMixin`
- Annotates `issues_count` via `Count`.

## `VolumesCountQuerySetMixin`
- Annotates `volumes_count` via `Count`.

## `FinishedQuerySetMixin`
- Adds `finished_count`, `max_finished_date`, `is_started`, `is_finished` for authenticated users.
- Leaves these values `null` for anonymous requests.

## `HideFinishedQuerySetMixin`
- When `action == "list"` and `?hide-finished=yes`, filters out resources where `is_finished=True`.
