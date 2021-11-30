from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class VolumesConfig(AppConfig):
    name = 'read_comics.volumes'

    def ready(self):
        model = self.get_model('Volume')
        watson.register(
            model,
            search_adapters.VolumeSearchAdapter,
            store=('name', 'short_description', 'thumb_url', 'start_year')
        )
