from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Publisher


class PublisherFactory(ComicvineSyncModelFactory):
    name = Faker("company")
    short_description = Faker("paragraph")

    class Meta:
        model = Publisher
