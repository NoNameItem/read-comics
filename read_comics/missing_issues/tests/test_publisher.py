import pytest

from read_comics.missing_issues.models import IgnoredVolume, MissingIssue
from read_comics.missing_issues.tasks import publisher_missing_issues_task
from read_comics.publishers.models import Publisher
from read_comics.volumes.models import Volume

pytestmark = pytest.mark.django_db


def test_publisher_filter_skips_ignored_volumes_and_caches_volumes(mongo_db, volumes_col):
    publisher = Publisher.objects.create(comicvine_id=500, name="Pub")
    volumes_col.insert_many(
        [
            {"id": 100, "name": "A", "publisher": {"id": 500, "name": "Pub"}},
            {"id": 101, "name": "B", "publisher": {"id": 500, "name": "Pub"}},
            {"id": 102, "name": "C", "publisher": {"id": 501, "name": "Other"}},
        ]
    )
    IgnoredVolume.objects.create(comicvine_id=101, name="B")
    volumes = {}
    assert publisher_missing_issues_task.get_object_filter(mongo_db, publisher, volumes) == {
        "volume.id": {"$in": [100]}
    }
    assert set(volumes) == {100, 101}


def test_publisher_run_end_to_end(mongo_db, issues_col, volumes_col, make_issue):
    publisher = Publisher.objects.create(comicvine_id=500, name="Pub")
    volume = Volume.objects.create(comicvine_id=100, name="A", publisher=publisher)
    make_issue(11, volume=volume)  # existing issue of the publisher
    volumes_col.insert_one({"id": 100, "name": "A", "start_year": "1990", "publisher": {"id": 500, "name": "Pub"}})
    issues_col.insert_many([{"id": 10, "volume": {"id": 100}}, {"id": 11, "volume": {"id": 100}}])
    publisher_missing_issues_task.run(pk=publisher.pk)
    assert list(MissingIssue.objects.values_list("comicvine_id", "publisher_id", "volume_start_year")) == [
        (10, publisher.pk, "1990")
    ]
