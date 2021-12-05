from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class ObjectsConfig(AppConfig):
    name = 'read_comics.objects'

    def ready(self):
        model = self.get_model('Object')
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED),
            search_adapters.ObjectSearchAdapter
        )
