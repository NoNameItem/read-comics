import factory
from factory import Faker
from factory.django import DjangoModelFactory

from ..models import MissingIssue


class MissingIssueFactory(DjangoModelFactory):
    comicvine_id = factory.Sequence(lambda n: n)
    comicvine_url = Faker("uri")
    name = Faker("word")
    number_int = Faker("pyint")
    number = factory.LazyAttribute(lambda o: str(o.number_int))
    cover_date = Faker("date_this_century")

    volume_comicvine_id = factory.Sequence(lambda n: n)
    volume_comicvine_url = Faker("uri")
    volume_name = Faker("word")
    volume_start_year = Faker("year")

    publisher_name = Faker("company")
    publisher_comicvine_id = factory.Sequence(lambda n: n)
    publisher_comicvine_url = Faker("uri")

    volume = factory.SubFactory("read_comics.volumes.tests.factories.VolumeFactory")
    publisher = factory.SubFactory("read_comics.publishers.tests.factories.PublisherFactory")

    class Meta:
        model = MissingIssue
        exclude = ["number_int"]
