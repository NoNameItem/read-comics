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

    first_issue = factory.SubFactory("read_comics.issues.tests.factories.IssueFactory")

    class Meta:
        model = Character
