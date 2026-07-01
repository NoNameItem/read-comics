import random

import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Volume


class VolumeFactory(ComicvineSyncModelFactory):
    name = Faker("word")
    short_description = Faker("paragraph")
    start_year_str = Faker("year")
    start_year = factory.LazyAttribute(lambda o: int(o.start_year_str))
    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")

    @factory.post_generation
    def add_issues(self: Volume, create, extracted, **kwargs):
        if create and extracted is not None and extracted > 0:
            from read_comics.issues.tests.factories import IssueFactory

            issues = IssueFactory.create_batch(size=extracted, volume=self)
            self.first_issue = random.choice(issues)
            self.save()

    class Meta:
        model = Volume
        exclude = ["start_year_str"]
