from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Person


class PersonFactory(ComicvineSyncModelFactory):
    name = Faker("name")
    short_description = Faker("paragraph")
    birth_date = Faker("date_this_century")
    hometown = Faker("city")
    country = Faker("country")

    class Meta:
        model = Person
