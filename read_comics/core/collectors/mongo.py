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

        self._set_metric("read_comics_mongo_count", {"collection": "total", "source": "all"}, 0)
        self._set_metric("read_comics_mongo_count", {"collection": "total", "source": "list"}, 0)
        self._set_metric("read_comics_mongo_count", {"collection": "total", "source": "detail"}, 0)

        for k, v in self.COLLECTIONS.items():
            count = self.db[v].count_documents({})
            list_count = self.db[v].count_documents({"crawl_source": "list"})
            detail_count = self.db[v].count_documents({"crawl_source": "detail"})

            self._set_metric("read_comics_mongo_count", {"collection": k, "source": "all"}, count)
            self._set_metric("read_comics_mongo_count", {"collection": k, "source": "list"}, list_count)
            self._set_metric("read_comics_mongo_count", {"collection": k, "source": "detail"}, detail_count)

            self._increment_metric("read_comics_mongo_count", {"collection": "total", "source": "all"}, count)
            self._increment_metric("read_comics_mongo_count", {"collection": "total", "source": "list"}, list_count)
            self._increment_metric("read_comics_mongo_count", {"collection": "total", "source": "detail"}, detail_count)
