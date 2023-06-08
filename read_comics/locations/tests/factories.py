import random

import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Location


class LocationFactory(ComicvineSyncModelFactory):
    name = Faker("city")
    short_description = Faker("paragraph")
    start_year = Faker("year")

    first_issue = factory.SubFactory("read_comics.issues.tests.factories.IssueFactory")

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
