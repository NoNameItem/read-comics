import random

import factory
from factory import Faker
from factory.fuzzy import FuzzyChoice
from utils.test_utils.factories import ComicvineSyncModelFactory

from read_comics.powers.tests.factories import PowerFactory

from ..models import Character


class CharacterFactory(ComicvineSyncModelFactory):
    name = Faker("name")
    real_name = Faker("name")
    short_description = Faker("paragraph")
    gender = FuzzyChoice(Character.Gender.choices, getter=lambda c: c[0])
    birth = Faker("date_this_century")
    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")
    first_issue_name = Faker("word")
    aliases_list = Faker("words", nb=6)
    aliases = factory.LazyAttribute(lambda o: "\n".join(o.aliases_list))

    @factory.post_generation
    def add_issues(self: Character, create, extracted, **kwargs):
        if create and extracted is not None and extracted > 0:
            from read_comics.issues.tests.factories import IssueFactory

            issues = IssueFactory.create_batch(size=extracted)
            self.issues.set(issues)
            self.first_issue = random.choice(issues)
            self.save()

    @factory.post_generation
    def add_powers(self: Character, create, extracted, **kwargs):
        if create:
            powers = PowerFactory.create_batch(size=random.randint(1, 3))
            self.powers.set(powers)

    class Meta:
        model = Character
        exclude = ["aliases_list"]
