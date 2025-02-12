from django.db.models import Count

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.issues.models import Issue
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.powers.models import Power
from read_comics.publishers.models import Publisher
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume

from .base import BaseCollector


class DBCollector(BaseCollector):
    MODELS = {
        "characters": Character,
        "concepts": Concept,
        "issues": Issue,
        "locations": Location,
        "objects": Object,
        "people": Person,
        "powers": Power,
        "publishers": Publisher,
        "story_arcs": StoryArc,
        "teams": Team,
        "volumes": Volume,
    }

    def collect(self):
        self._register_metric("read_comics_db_count", help_string="Number of rows in database")

        self._set_metric("read_comics_db_count", {"table": "total", "status": "all"}, 0)
        self._set_metric("read_comics_db_count", {"table": "total", "status": "matched"}, 0)
        self._set_metric("read_comics_db_count", {"table": "total", "status": "not_matched"}, 0)
        self._set_metric("read_comics_db_count", {"table": "total", "status": "queued"}, 0)

        for k, v in self.MODELS.items():
            counts = dict(
                v.objects.values("comicvine_status")
                .annotate(count=Count("id"))
                .order_by()
                .values_list("comicvine_status", "count")
            )

            total = sum(counts.values())

            self._set_metric("read_comics_db_count", {"table": k, "status": "all"}, total)
            self._set_metric("read_comics_db_count", {"table": k, "status": "matched"}, counts.get("MATCHED", 0))
            self._set_metric(
                "read_comics_db_count", {"table": k, "status": "not_matched"}, counts.get("NOT_MATCHED", 0)
            )
            self._set_metric("read_comics_db_count", {"table": k, "status": "queued"}, counts.get("QUEUED", 0))

            self._increment_metric("read_comics_db_count", {"table": "total", "status": "all"}, total)
            self._increment_metric(
                "read_comics_db_count", {"table": "total", "status": "matched"}, counts.get("MATCHED", 0)
            )
            self._increment_metric(
                "read_comics_db_count", {"table": "total", "status": "not_matched"}, counts.get("NOT_MATCHED", 0)
            )
            self._increment_metric(
                "read_comics_db_count", {"table": "total", "status": "queued"}, counts.get("QUEUED", 0)
            )
