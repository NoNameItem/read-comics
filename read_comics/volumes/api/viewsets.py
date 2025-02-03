from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Volume


class VolumeStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_volumes"
    model = Volume
