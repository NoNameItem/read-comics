from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class PublishersConfig(AppConfig):
    name = "read_comics.publishers"

    def ready(self):
        model = self.get_model("Publisher")
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED), search_adapters.PublisherSearchAdapter
        )
