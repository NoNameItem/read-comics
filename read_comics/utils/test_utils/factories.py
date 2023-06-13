import factory
from django.utils import timezone
from factory import Faker
from factory.django import DjangoModelFactory
from utils.models import ComicvineSyncModel


class ComicvineSyncModelFactory(DjangoModelFactory):
    comicvine_id = factory.Sequence(lambda n: n)
    comicvine_url = Faker("uri")
    comicvine_status = ComicvineSyncModel.ComicvineStatus.MATCHED
    comicvine_last_match = Faker("date_time_this_year", tzinfo=timezone.get_current_timezone())
    created_dt = Faker("date_time_this_year", tzinfo=timezone.get_current_timezone())
    modified_dt = Faker("date_time_this_year", tzinfo=timezone.get_current_timezone())

    class Meta:
        django_get_or_create = ["comicvine_id"]
