import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Person


class PersonFactory(ComicvineSyncModelFactory):
    name = Faker("name")
    short_description = Faker("paragraph")
    birth_date = Faker("date_this_century")
    hometown = Faker("city")
    country = Faker("country")

    @factory.post_generation
    def add_issues(self: Person, create, extracted, **kwargs):
        if create and extracted is not None and extracted > 0:
            from read_comics.issues.tests.factories import IssuePersonFactory

            issues = IssuePersonFactory.create_batch(size=extracted, person=self)
            self.authored_issues.set(issues)

    class Meta:
        model = Person
