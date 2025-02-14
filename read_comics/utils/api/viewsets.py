from django.conf import settings
from pymongo import MongoClient
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import ComicvineSyncModel


class BaseStatsViewSet(viewsets.ViewSet):
    mongo_collection: str
    model: ComicvineSyncModel

    @action(detail=False, methods=["GET"])
    def mongo_count(self, request):
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[self.mongo_collection]
        data = {"count": collection.count_documents({})}
        client.close()
        return Response(data=data)

    @action(detail=False, methods=["GET"])
    def mongo_list_count(self, request):
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[self.mongo_collection]
        data = {"count": collection.count_documents({"crawl_source": "list"})}
        client.close()
        return Response(data=data)

    @action(detail=False, methods=["GET"])
    def mongo_detail_count(self, request):
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[self.mongo_collection]
        data = {"count": collection.count_documents({"crawl_source": "detail"})}
        client.close()
        return Response(data=data)

    @action(detail=False, methods=["GET"])
    def db_count(self, request):
        return Response(data={"count": self.model.objects.count()})

    @action(detail=False, methods=["GET"])
    def matched_count(self, request):
        return Response(data={"count": self.model.objects.matched().count()})

    @action(detail=False, methods=["GET"])
    def not_matched_count(self, request):
        return Response(data={"count": self.model.objects.not_matched().count()})

    @action(detail=False, methods=["GET"])
    def queued_count(self, request):
        return Response(data={"count": self.model.objects.queued().count()})
