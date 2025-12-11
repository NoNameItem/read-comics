from datetime import datetime

from django.db import migrations
from django.db.migrations import RunPython


def create_comicvine_lock(apps, schema_editor):
    Locks = apps.get_model("missing_issues", "Locks")
    lock = Locks(code="COMICVINE_LOCK", dttm=datetime.now())
    lock.save()


class Migration(migrations.Migration):

    dependencies = [
        ("missing_issues", "0013_locks"),
    ]

    operations = [
        RunPython(create_comicvine_lock),
    ]
