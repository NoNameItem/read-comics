import random

import factory
from factory import Faker
from factory.fuzzy import FuzzyChoice
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Character


class CharacterFactory(ComicvineSyncModelFactory):
    name = Faker("name")
    real_name = Faker("name")
    short_description = Faker("paragraph")
    gender = FuzzyChoice(Character.Gender.choices, getter=lambda c: c[0])
    birth = Faker("date_this_century")
    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")

    @factory.post_generation
    def add_issues(self: Character, create, extracted, **kwargs):
        if create and extracted is not None and extracted > 0:
            from read_comics.issues.tests.factories import IssueFactory

            issues = IssueFactory.create_batch(size=extracted)
            self.issues.set(issues)
            self.first_issue = random.choice(issues)
            self.save()

    class Meta:
        model = Character
