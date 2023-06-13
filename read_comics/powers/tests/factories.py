from factory import Faker
from utils.test_utils.factories import ComicvineSyncModelFactory

from ..models import Power


class PowerFactory(ComicvineSyncModelFactory):
    name = Faker("job")

    class Meta:
        model = Power
