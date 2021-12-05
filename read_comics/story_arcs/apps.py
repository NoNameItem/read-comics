from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class StoryArcsConfig(AppConfig):
    name = 'read_comics.story_arcs'

    def ready(self):
        model = self.get_model('StoryArc')
        watson.register(
            model.objects.filter(comicvine_status=model.ComicvineStatus.MATCHED),
            search_adapters.StoryArcSearchAdapter
        )
