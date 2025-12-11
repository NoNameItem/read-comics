from django.db.models import Count

from read_comics.core.collectors.base import BaseCollector
from read_comics.missing_issues.models import APIQueue


class ApiQueueCollector(BaseCollector):
    def collect(self):
        queues = APIQueue.objects.values("endpoint").annotate(count=Count("comicvine_id"))

        self._register_metric("read_comics_api_queue_count", help_string="Number of items in comicvine API queue")

        for queue in queues:
            self._set_metric("read_comics_api_queue_count", {"endpoint": queue["endpoint"]}, queue["count"])
