import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Team


class TeamFactory(ComicvineSyncModelFactory):
    name = Faker("company")
    short_description = Faker("paragraph")
    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")

    first_issue = factory.SubFactory("read_comics.issues.tests.factories.IssueFactory")

    class Meta:
        model = Team
