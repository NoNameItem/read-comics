import factory
from factory import Faker
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory
from utils.test_utils.factories import ComicvineSyncModelFactory

from read_comics.issues.models import FinishedIssue, Issue, IssuePerson


class IssueFactory(ComicvineSyncModelFactory):
    name = Faker("words")
    short_description = Faker("paragraph")
    number_int = Faker("pyint")
    number = factory.LazyAttribute(lambda o: str(o.number_int))
    cover_date = Faker("date_this_decade")
    store_date = Faker("date_this_decade")
    size = Faker("pyint")

    volume = factory.SubFactory("read_comics.volumes.tests.factories.VolumeFactory")

    class Meta:
        model = Issue
        exclude = ["number_int"]


class IssuePersonFactory(DjangoModelFactory):
    issue = factory.SubFactory(IssueFactory)
    person = factory.SubFactory("read_comics.people.tests.factories.PersonFactory")
    role = Faker("job")

    class Meta:
        model = IssuePerson


class FinishedIssueFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    issue = factory.SubFactory(IssueFactory)
    finish_date = Faker("date_this_decade")

    class Meta:
        model = FinishedIssue
