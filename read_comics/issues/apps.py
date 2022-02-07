from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class IssuesConfig(AppConfig):
    name = "read_comics.issues"

    def ready(self):
        model = self.get_model("Issue")
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED),
            search_adapters.IssueSearchAdapter
        )
