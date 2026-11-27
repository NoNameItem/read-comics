from datetime import timedelta
from itertools import islice

from django.conf import settings
from django.db import migrations, models
from django.utils import timezone


def migrate_skip_until(apps, schema_editor):
    missing_issue = apps.get_model("missing_issues", "MissingIssue")
    skipped = missing_issue.objects.using(schema_editor.connection.alias).filter(skip=True)
    today = timezone.localdate()
    offset = timedelta(days=settings.SKIP_DAYS + 1)
    batch_size = 500
    rows = skipped.only("skip_date").iterator(chunk_size=batch_size)
    while batch := list(islice(rows, batch_size)):
        for issue in batch:
            issue.skip_until = (issue.skip_date or today) + offset
        skipped.bulk_update(batch, ["skip_until"], batch_size=batch_size)


class Migration(migrations.Migration):
    dependencies = [("missing_issues", "0018_alter_apiqueue_comicvine_id")]

    operations = [
        migrations.AddField(
            model_name="missingissue",
            name="skip_until",
            field=models.DateField(null=True),
        ),
        migrations.RunPython(migrate_skip_until, migrations.RunPython.noop),
    ]
