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
            counts_query = self.db[v].aggregate([{"$group": {"_id": "$crawl_source", "count": {"$sum": 1}}}])

            counts = dict([i.values() for i in counts_query])

            total_count = sum(counts.values())

            self._set_metric("read_comics_mongo_count", {"collection": k, "source": "all"}, total_count)
            self._set_metric("read_comics_mongo_count", {"collection": k, "source": "list"}, counts.get("list", 0))
            self._set_metric("read_comics_mongo_count", {"collection": k, "source": "detail"}, counts.get("detail", 0))

            self._increment_metric("read_comics_mongo_count", {"collection": "total", "source": "all"}, total_count)
            self._increment_metric(
                "read_comics_mongo_count", {"collection": "total", "source": "list"}, counts.get("list", 0)
            )
            self._increment_metric(
                "read_comics_mongo_count", {"collection": "total", "source": "detail"}, counts.get("detail", 0)
            )
