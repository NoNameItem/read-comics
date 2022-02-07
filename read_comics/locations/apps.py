from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class LocationsConfig(AppConfig):
    name = "read_comics.locations"

    def ready(self):
        model = self.get_model("Location")
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED),
            search_adapters.LocationSearchAdapter
        )
