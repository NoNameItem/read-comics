from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Publisher


class PublisherStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_publishers"
    model = Publisher
