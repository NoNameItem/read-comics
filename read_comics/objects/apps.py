from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class ObjectsConfig(AppConfig):
    name = 'read_comics.objects'

    def ready(self):
        publisher_model = self.get_model('Object')
        watson.register(
            publisher_model,
            search_adapters.ObjectSearchAdapter,
            store=('name', 'short_description', 'thumb_url')
        )
