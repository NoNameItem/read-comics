from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class ConceptsConfig(AppConfig):
    name = "read_comics.concepts"

    def ready(self):
        model = self.get_model("Concept")
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED), search_adapters.ConceptSearchAdapter
        )
