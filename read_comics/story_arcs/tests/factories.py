import random

import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import StoryArc


class StoryArcFactory(ComicvineSyncModelFactory):
    name = Faker("name")
    short_description = Faker("paragraph")

    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")

    @factory.post_generation
    def add_issues(self: StoryArc, create, extracted, **kwargs):
        if create and extracted is not None and extracted > 0:
            from read_comics.issues.tests.factories import IssueFactory

            issues = IssueFactory.create_batch(size=extracted, volume__publisher=self.publisher)
            self.issues.set(issues)
            self.first_issue = random.choice(issues)
            self.save()

    class Meta:
        model = StoryArc
