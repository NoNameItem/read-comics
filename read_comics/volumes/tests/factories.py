import factory
from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Volume


class VolumeFactory(ComicvineSyncModelFactory):
    name = Faker("word")
    short_description = Faker("paragraph")
    start_year = Faker("year")
    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")

    class Meta:
        model = Volume
