from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class TeamsConfig(AppConfig):
    name = "read_comics.teams"

    def ready(self):
        model = self.get_model("Team")
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED),
            search_adapters.TeamSearchAdapter
        )
