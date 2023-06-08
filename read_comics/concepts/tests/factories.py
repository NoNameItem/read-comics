import random

import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Concept


class ConceptFactory(ComicvineSyncModelFactory):
    name = Faker("word")
    short_description = Faker("paragraph")
    start_year = Faker("year")

    @factory.post_generation
    def add_issues(self: Concept, create, extracted, **kwargs):
        if create and extracted is not None and extracted > 0:
            from read_comics.issues.tests.factories import IssueFactory

            issues = IssueFactory.create_batch(size=extracted)
            self.issues.set(issues)
            self.first_issue = random.choice(issues)
            self.save()

    class Meta:
        model = Concept
