import pytest

from read_comics.missing_issues.tasks import character_missing_issues_task

pytestmark = pytest.mark.usefixtures("run_caches")

CANDIDATE = {
    "id": 10,
    "volume_id": 100,
    "site_detail_url": "https://cv/i10",
    "name": "N",
    "issue_number": "1",
    "cover_date": "2020-01-31",
}
VOLUME = {
    "id": 100,
    "site_detail_url": "https://cv/v100",
    "name": "Vol",
    "start_year": "1940",
    "publisher": {"id": 500, "name": "Pub"},
}


def rows_for(mongo_db, candidates):
    task = character_missing_issues_task
    task.load_volumes(mongo_db, [c["volume_id"] for c in candidates])
    task.load_publishers(mongo_db, [task.get_volume_publisher(c["volume_id"]).get("id") for c in candidates])
    return task.get_rows(candidates)


def test_rows_full_join(mongo_db, volumes_col, publishers_col):
    volumes_col.insert_one(dict(VOLUME))
    publishers_col.insert_one({"id": 500, "site_detail_url": "https://cv/p500"})
    assert rows_for(mongo_db, [dict(CANDIDATE)]) == [
        {
            "comicvine_id": 10,
            "comicvine_url": "https://cv/i10",
            "name": "N",
            "number": "1",
            "cover_date": "2020-01-31",
            "volume_comicvine_id": 100,
            "volume_comicvine_url": "https://cv/v100",
            "volume_name": "Vol",
            "volume_start_year": "1940",
            "publisher_name": "Pub",
            "publisher_comicvine_id": 500,
            "publisher_comicvine_url": "https://cv/p500",
        }
    ]


def test_rows_volume_doc_missing(mongo_db):
    [row] = rows_for(mongo_db, [dict(CANDIDATE)])
    assert row["name"] == "N"
    assert all(row[k] is None for k in row if k.startswith(("volume_", "publisher_")))


def test_rows_publisher_doc_missing(mongo_db, volumes_col):
    volumes_col.insert_one(dict(VOLUME))
    [row] = rows_for(mongo_db, [dict(CANDIDATE)])
    assert (row["publisher_name"], row["publisher_comicvine_id"], row["publisher_comicvine_url"]) == ("Pub", 500, None)


def test_rows_absent_issue_fields_are_none(mongo_db):
    [row] = rows_for(mongo_db, [{"id": 10, "volume_id": None}])
    assert row["name"] is None and row["number"] is None and row["cover_date"] is None
    assert len(row) == 12
