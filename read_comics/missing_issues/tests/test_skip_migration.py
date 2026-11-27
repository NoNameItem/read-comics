from datetime import date

import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


@pytest.mark.django_db(transaction=True)
def test_migrate_skip_until(monkeypatch, settings):
    source = [("missing_issues", "0018_alter_apiqueue_comicvine_id")]
    target = [("missing_issues", "0020_remove_legacy_skip_fields")]
    monkeypatch.setattr("django.utils.timezone.localdate", lambda: date(2026, 3, 1))
    settings.SKIP_DAYS = 7
    old_apps = MigrationExecutor(connection).migrate(source).apps
    old_issue = old_apps.get_model("missing_issues", "MissingIssue")

    old_issue.objects.create(comicvine_id=10)
    old_issue.objects.create(comicvine_id=11, skip_date=date(2026, 2, 20))
    old_issue.objects.create(comicvine_id=12, skip=True, skip_date=date(2026, 2, 20))
    old_issue.objects.create(comicvine_id=13, skip=True)

    new_apps = MigrationExecutor(connection).migrate(target).apps
    new_issue = new_apps.get_model("missing_issues", "MissingIssue")
    assert dict(new_issue.objects.values_list("comicvine_id", "skip_until")) == {
        10: None,
        11: None,
        12: date(2026, 2, 28),
        13: date(2026, 3, 9),
    }
