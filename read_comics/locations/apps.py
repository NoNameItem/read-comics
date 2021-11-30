from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class LocationsConfig(AppConfig):
    name = 'read_comics.locations'

    def ready(self):
        publisher_model = self.get_model('Location')
        watson.register(
            publisher_model,
            search_adapters.LocationSearchAdapter,
            store=('name', 'short_description', 'thumb_url')
        )
