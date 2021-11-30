from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class ConceptsConfig(AppConfig):
    name = 'read_comics.concepts'

    def ready(self):
        publisher_model = self.get_model('Concept')
        watson.register(
            publisher_model,
            search_adapters.ConceptSearchAdapter,
            store=('name', 'short_description', 'thumb_url')
        )
