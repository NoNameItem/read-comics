import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Concept


class ConceptFactory(ComicvineSyncModelFactory):
    name = Faker("word")
    short_description = Faker("paragraph")
    start_year = Faker("year")

    first_issue = factory.SubFactory("read_comics.issues.tests.factories.IssueFactory")

    class Meta:
        model = Concept
