from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class PeopleConfig(AppConfig):
    name = "read_comics.people"

    def ready(self):
        model = self.get_model("Person")
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED), search_adapters.PersonSearchAdapter
        )
