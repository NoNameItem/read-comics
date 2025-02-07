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
        self._register_metric(
            "read_comics_db_matched_count", help_string="Number of rows in database matched with comicvine"
        )
        self._register_metric(
            "read_comics_db_not_matched_count", help_string="Number of rows in database not_matched with comicvine"
        )
        self._register_metric(
            "read_comics_db_queued_count", help_string="Number of rows in database queued for matching"
        )

        self._set_metric("read_comics_db_count", {"table": "total"}, 0)
        self._set_metric("read_comics_db_matched_count", {"table": "total"}, 0)
        self._set_metric("read_comics_db_not_matched_count", {"table": "total"}, 0)
        self._set_metric("read_comics_db_queued_count", {"table": "total"}, 0)

        for k, v in self.MODELS.items():
            count = v.objects.all().count()
            matched_count = v.objects.matched().count()
            not_matched_count = v.objects.not_matched().count()
            queued_count = v.objects.queued().count()

            self._set_metric("read_comics_db_count", {"table": k}, count)
            self._set_metric("read_comics_db_matched_count", {"table": k}, matched_count)
            self._set_metric("read_comics_db_not_matched_count", {"table": k}, not_matched_count)
            self._set_metric("read_comics_db_queued_count", {"table": k}, queued_count)

            self._increment_metric("read_comics_db_count", {"table": "total"}, count)
            self._increment_metric("read_comics_db_matched_count", {"table": "total"}, matched_count)
            self._increment_metric("read_comics_db_not_matched_count", {"table": "total"}, not_matched_count)
            self._increment_metric("read_comics_db_queued_count", {"table": "total"}, queued_count)
