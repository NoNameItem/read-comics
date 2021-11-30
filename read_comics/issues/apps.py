from django.apps import AppConfig
from watson import search as watson

from . import search_adapters


class IssuesConfig(AppConfig):
    name = 'read_comics.issues'

    def ready(self):
        publisher_model = self.get_model('Issue')
        watson.register(
            publisher_model,
            search_adapters.IssueSearchAdapter,
            store=('name', 'short_description', 'thumb_url', 'number')
        )
