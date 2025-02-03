from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Team


class TeamStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_teams"
    model = Team
