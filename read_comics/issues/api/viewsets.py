from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Issue


class IssueStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_issues"
    model = Issue
