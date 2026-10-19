from read_comics.missing_issues.tasks import character_missing_issues_task

ISSUE = {
    "id": 10,
    "volume": {"id": 100},
    "character_credits": [{"id": 1699}],
    "site_detail_url": "https://cv/i10",
    "name": "N",
    "issue_number": "1",
    "cover_date": "2020-01-31",
    "description": "dropped",
}
VOLUME = {
    "id": 100,
    "site_detail_url": "https://cv/v100",
    "name": "Vol",
    "start_year": "1940",
    "publisher": {"id": 500, "name": "Pub"},
}
FILTER = {"character_credits.id": 1699}


def rows_for(mongo_db, candidates):
    volumes = {}
    task = character_missing_issues_task
    task.load_volumes(mongo_db, [c["volume_id"] for c in candidates], volumes)
    return task.get_rows(mongo_db, FILTER, candidates, volumes)


def test_rows_full_join(mongo_db, issues_col, volumes_col, publishers_col):
    issues_col.insert_one(dict(ISSUE))
    volumes_col.insert_one(dict(VOLUME))
    publishers_col.insert_one({"id": 500, "site_detail_url": "https://cv/p500"})
    assert rows_for(mongo_db, [{"id": 10, "volume_id": 100}]) == [
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


def test_rows_volume_doc_missing(mongo_db, issues_col):
    issues_col.insert_one(dict(ISSUE))
    [row] = rows_for(mongo_db, [{"id": 10, "volume_id": 100}])
    assert row["name"] == "N"
    assert all(row[k] is None for k in row if k.startswith(("volume_", "publisher_")))


def test_rows_publisher_doc_missing(mongo_db, issues_col, volumes_col):
    issues_col.insert_one(dict(ISSUE))
    volumes_col.insert_one(dict(VOLUME))
    [row] = rows_for(mongo_db, [{"id": 10, "volume_id": 100}])
    assert (row["publisher_name"], row["publisher_comicvine_id"], row["publisher_comicvine_url"]) == ("Pub", 500, None)


def test_rows_absent_issue_fields_are_none(mongo_db, issues_col):
    issues_col.insert_one({"id": 10, "character_credits": [{"id": 1699}]})
    [row] = rows_for(mongo_db, [{"id": 10, "volume_id": None}])
    assert row["name"] is None and row["number"] is None and row["cover_date"] is None
    assert len(row) == 12


def test_rows_use_document_with_object_credit(mongo_db, issues_col):
    issues_col.insert_many([dict(ISSUE), {"id": 10, "name": "stale copy without credit"}])
    [row] = rows_for(mongo_db, [{"id": 10, "volume_id": 100}])
    assert row["name"] == "N"


def test_rows_sorted_by_comicvine_id(mongo_db, issues_col):
    issues_col.insert_many([{**ISSUE, "id": 30}, {**ISSUE, "id": 10}, {**ISSUE, "id": 20}])
    rows = rows_for(mongo_db, [{"id": i, "volume_id": 100} for i in (30, 10, 20)])
    assert [row["comicvine_id"] for row in rows] == [10, 20, 30]
