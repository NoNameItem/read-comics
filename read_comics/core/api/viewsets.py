from typing import Callable, Type, TypeVar

from django.conf import settings
from pymongo import MongoClient
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.issues.models import Issue
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.powers.models import Power
from read_comics.publishers.models import Publisher
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.utils.models import ComicvineSyncModel
from read_comics.volumes.models import Volume


class ExtraKeyError(Exception):
    def __init__(self, keys):
        super().__init__()
        self.keys = keys


T = TypeVar("T")


class CoreStatsViewSet(viewsets.ViewSet):
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

    MODELS = {
        "characters": Character,
        "concepts": Concept,
        "issues": Issue,
        "locations": Location,
        "objects": Object,
        "people": Person,
        "powers": Power,
        "publishers": Publisher,
        "story_arcs": StoryArc,
        "teams": Team,
        "volumes": Volume,
    }

    @staticmethod
    def _mongo_count(collection: str) -> int:
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[collection]
        count = collection.count_documents({})
        client.close()
        return count  # noqa R504

    @staticmethod
    def _mongo_list_count(collection: str) -> int:
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[collection]
        count = collection.count_documents({"crawl_source": "list"})
        client.close()
        return count  # noqa R504

    @staticmethod
    def _mongo_detail_count(collection: str) -> int:
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[collection]
        count = collection.count_documents({"crawl_source": "detail"})
        client.close()
        return count  # noqa R504

    @staticmethod
    def _db_count(model: Type[ComicvineSyncModel]) -> int:
        return model.objects.count()

    @staticmethod
    def _matched_count(model: Type[ComicvineSyncModel]) -> int:
        return model.objects.matched().count()

    @staticmethod
    def _not_matched_count(model: Type[ComicvineSyncModel]) -> int:
        return model.objects.not_matched().count()

    @staticmethod
    def _queued_count(model: Type[ComicvineSyncModel]) -> int:
        return model.objects.queued().count()

    @staticmethod
    def _reduce_mongo(collections: list[str], method: Callable[[str], int]) -> int:
        result = 0

        for collection in collections:
            result += method(collection)

        return result

    @staticmethod
    def _reduce_db(models: list[ComicvineSyncModel], method: Callable[[Type[ComicvineSyncModel]], int]) -> int:
        result = 0

        for model in models:
            result += method(model)

        return result

    def _get_keys(self, request: Request) -> list[str]:
        potential_keys = request.query_params.getlist("var-keys")

        if not potential_keys:
            return list(self.COLLECTIONS.keys())

        extra_keys = [key for key in potential_keys if key not in self.COLLECTIONS]

        if extra_keys:
            raise ExtraKeyError(extra_keys)

        return potential_keys

    @staticmethod
    def _filter_by_keys(
        d: dict[str, T] | dict[str, ComicvineSyncModel],
        keys: list[str],
    ) -> list[T] | list[ComicvineSyncModel]:
        if not keys:
            return list(d.values())

        return [d[key] for key in keys]

    def _process_mongo(self, request: Request, method: Callable[[str], int]) -> Response:
        try:
            keys = self._get_keys(request)
            collections = self._filter_by_keys(self.COLLECTIONS, keys)
            count = self._reduce_mongo(collections, method)
            return Response({"count": count})
        except ExtraKeyError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": f"Found wrong keys: {e.keys}. Available keys: {list(self.COLLECTIONS.keys())}",
                },
            )

    def _process_db(self, request: Request, method: Callable[[Type[ComicvineSyncModel]], int]) -> Response:
        try:
            keys = self._get_keys(request)
            models = self._filter_by_keys(self.MODELS, keys)
            count = self._reduce_db(models, method)
            return Response({"count": count})
        except ExtraKeyError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": f"Found wrong keys: {e.keys}. Available keys: {list(self.COLLECTIONS.keys())}",
                },
            )

    @action(detail=False, methods=["GET"])
    def mongo_count(self, request: Request) -> Response:
        return self._process_mongo(request, self._mongo_count)

    @action(detail=False, methods=["GET"])
    def mongo_list_count(self, request: Request) -> Response:
        return self._process_mongo(request, self._mongo_list_count)

    @action(detail=False, methods=["GET"])
    def mongo_detail_count(self, request: Request) -> Response:
        return self._process_mongo(request, self._mongo_detail_count)

    @action(detail=False, methods=["GET"])
    def db_count(self, request: Request) -> Response:
        return self._process_db(request, self._db_count)

    @action(detail=False, methods=["GET"])
    def matched_count(self, request: Request) -> Response:
        return self._process_db(request, self._matched_count)

    @action(detail=False, methods=["GET"])
    def not_matched_count(self, request: Request) -> Response:
        return self._process_db(request, self._not_matched_count)

    @action(detail=False, methods=["GET"])
    def queued_count(self, request: Request) -> Response:
        return self._process_db(request, self._queued_count)
