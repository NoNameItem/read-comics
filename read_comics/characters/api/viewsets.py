from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Character


class CharacterStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_characters"
    model = Character
