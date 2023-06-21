import random

import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Publisher


class PublisherFactory(ComicvineSyncModelFactory):
    name = Faker("company")
    short_description = Faker("paragraph")

    @factory.post_generation
    def add_volumes(self: Publisher, create, extracted, **kwargs):
        if create and extracted is not None and extracted > 0:
            from read_comics.volumes.tests.factories import VolumeFactory

            VolumeFactory.create_batch(size=extracted, publisher=self, add_issues=random.randrange(1, 5))

    class Meta:
        model = Publisher
