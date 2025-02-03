from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Power


class PowerStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_powers"
    model = Power
