from read_comics.utils.api.viewsets import BaseStatsViewSet

from ..models import Concept


class ConceptStatsViewSet(BaseStatsViewSet):
    mongo_collection = "comicvine_concepts"
    model = Concept
