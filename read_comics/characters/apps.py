from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class CharactersConfig(AppConfig):
    name = 'read_comics.characters'

    def ready(self):
        model = self.get_model('Character')
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED),
            search_adapters.CharacterSearchAdapter
        )
