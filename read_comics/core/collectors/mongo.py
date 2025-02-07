from django.conf import settings
from pymongo import MongoClient

from .base import BaseCollector


class MongoCollector(BaseCollector):
    COLLECTIONS = {
        "characters": "comicvine_characters",
        "concepts": "comicvine_concepts",
        "issues": "comicvine_issues",
        "locations": "comicvine_locations",
        "objects": "comicvine_objects",
        "people": "comicvine_people",
        "powers": "comicvine_powers",
        "publishers": "comicvine_publishers",
        "story_arcs": "comicvine_story_arcs",
        "teams": "comicvine_teams",
        "volumes": "comicvine_volumes",
    }

    def __init__(self):
        super().__init__()
        self.client = MongoClient(settings.MONGO_URL)
        self.db = self.client.get_default_database()

    def collect(self):
        self._register_metric("read_comics_mongo_count", help_string="Number of documents in mongo collection")
        self._register_metric(
            "read_comics_mongo_list_count",
            help_string="Number of documents in mongo collection crawled from list endpoint",
        )
        self._register_metric(
            "read_comics_mongo_detail_count",
            help_string="Number of documents in mongo collection crawled from detail endpoint",
        )

        self._set_metric("read_comics_mongo_count", {"collection": "total"}, 0)
        self._set_metric("read_comics_mongo_list_count", {"collection": "total"}, 0)
        self._set_metric("read_comics_mongo_detail_count", {"collection": "total"}, 0)

        for k, v in self.COLLECTIONS.items():
            count = self.db[v].count_documents({})
            list_count = self.db[v].count_documents({"crawl_source": "list"})
            detail_count = self.db[v].count_documents({"crawl_source": "detail"})

            self._set_metric("read_comics_mongo_count", {"collection": k}, count)
            self._set_metric("read_comics_mongo_list_count", {"collection": k}, list_count)
            self._set_metric("read_comics_mongo_detail_count", {"collection": k}, detail_count)

            self._increment_metric("read_comics_mongo_count", {"collection": "total"}, count)
            self._increment_metric("read_comics_mongo_list_count", {"collection": "total"}, list_count)
            self._increment_metric("read_comics_mongo_detail_count", {"collection": "total"}, detail_count)
