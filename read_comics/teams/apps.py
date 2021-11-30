from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class TeamsConfig(AppConfig):
    name = 'read_comics.teams'

    def ready(self):
        publisher_model = self.get_model('Team')
        watson.register(
            publisher_model,
            search_adapters.TeamSearchAdapter,
            store=('name', 'short_description', 'thumb_url')
        )
