from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Location


class LocationStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_locations"
    model = Location
