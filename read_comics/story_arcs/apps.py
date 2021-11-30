from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class StoryArcsConfig(AppConfig):
    name = 'read_comics.story_arcs'

    def ready(self):
        publisher_model = self.get_model('StoryArc')
        watson.register(
            publisher_model,
            search_adapters.StoryArcSearchAdapter,
            store=('name', 'short_description', 'thumb_url')
        )
