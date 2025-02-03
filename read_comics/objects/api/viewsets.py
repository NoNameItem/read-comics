from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Object


class ObjectStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_objects"
    model = Object
