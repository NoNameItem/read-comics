# Teams Celery Tasks

## Summary

- `TeamComicvineInfoTask` — Syncs team data from MongoDB to PostgreSQL
- `TeamsRefreshTask` — Full refresh of all teams from scratch
- 4 spider tasks — Different sync strategies

## Reference

### TeamComicvineInfoTask

Base Celery task for syncing team data from MongoDB cache to PostgreSQL database.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `MODEL_NAME` | `"Team"` | Django model class name |
| `APP_LABEL` | `"teams"` | Django app for model lookup |
| `MISSING_ISSUES_TASK` | `"read_comics.missing_issues.tasks.TeamMissingIssuesTask"` | Task to trigger missing issues detection after sync |

---

### TeamsRefreshTask

Full refresh task for all teams.

#### Configuration

| Setting | Value | Description |
|---|---|---|
| `MODEL_NAME` | `"Team"` | Django model class name |
| `APP_LABEL` | `"teams"` | Django app for model lookup |

---

### Spider Tasks (4 variants)

Four Celery tasks with different sync strategies:

| Task Name | Config | Behavior | Schedule |
|---|---|---|---|
| `teams_increment_update()` | incr=Y, skip=N | Modified teams, full data | Every 6-12 hours |
| `teams_skip_existing_increment_update()` | incr=Y, skip=Y | Modified teams, skip cached detail | Every 12-24 hours |
| `teams_skip_existing_update()` | incr=N, skip=Y | All teams, skip cached detail | As-needed |
| `teams_update()` | incr=N, skip=N | All teams, full refresh | Weekly/monthly |

## References

- [../models.md](../models.md) — Team model definition
- [../spiders/teams_spider.md](../spiders/teams_spider.md) — TeamsSpider configuration
- [../../utils/tasks.md](../../utils/tasks.md) — BaseComicvineInfoTask and BaseRefreshTask