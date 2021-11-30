from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class CharactersConfig(AppConfig):
    name = 'read_comics.characters'

    def ready(self):
        publisher_model = self.get_model('Character')
        watson.register(
            publisher_model,
            search_adapters.CharacterSearchAdapter,
            store=('name', 'short_description', 'thumb_url', 'real_name', 'publisher__name')
        )
