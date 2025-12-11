from datetime import datetime

from django.db import migrations
from django.db.migrations import RunPython


def create_comicvine_lock(apps, schema_editor):
    Locks = apps.get_model("missing_issues", "Locks")

    Locks.objects.filter(code="COMICVINE_LOCK").delete()

    lock = Locks(code="comicvine_characters", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_concepts", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_issues", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_locations", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_objects", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_people", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_powers", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_publishers", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_story_arcs", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_teams", dttm=datetime.now())
    lock.save()

    lock = Locks(code="comicvine_volumes", dttm=datetime.now())
    lock.save()


class Migration(migrations.Migration):

    dependencies = [
        ("missing_issues", "0014_comicvine_lock"),
    ]

    operations = [
        RunPython(create_comicvine_lock),
    ]
