from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import StoryArc


class StoryArcStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_story_arcs"
    model = StoryArc
