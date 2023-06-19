import random

import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Location


class LocationFactory(ComicvineSyncModelFactory):
    name = Faker("city")
    short_description = Faker("paragraph")
    start_year_str = Faker("year")
    start_year = factory.LazyAttribute(lambda o: int(o.start_year_str))
    aliases_list = Faker("words", nb=6)
    aliases = factory.LazyAttribute(lambda o: "\n".join(o.aliases_list))

    @factory.post_generation
    def add_issues(self: Location, create, extracted, **kwargs):
        if create and extracted is not None and extracted > 0:
            from read_comics.issues.tests.factories import IssueFactory

            issues = IssueFactory.create_batch(size=extracted)
            self.issues.set(issues)
            self.first_issue = random.choice(issues)
            self.save()

    class Meta:
        model = Location
        exclude = ["aliases_list", "start_year_str"]
