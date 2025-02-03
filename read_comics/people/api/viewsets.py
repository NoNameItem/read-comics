from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Person


class PersonStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_people"
    model = Person
