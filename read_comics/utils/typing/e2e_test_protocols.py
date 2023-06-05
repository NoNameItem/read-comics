# pylint: skip-file

from factory.django import DjangoModelFactory
from typing_extensions import Protocol

from read_comics.users.models import User


# Field check protocols
class HasFactory(Protocol):
    factory: DjangoModelFactory


class HasCountUrl(Protocol):
    count_url: str


class HasStartedUrl(Protocol):
    started_url: str


# Test Suites protocols
class CountTestSuite(HasFactory, HasCountUrl, Protocol):
    pass


class StartedTestSuite(HasFactory, HasStartedUrl, Protocol):
    @staticmethod
    def _generate_finished_issues(item, usr: User, finished_date_step: int = 0) -> None:
        ...

    @staticmethod
    def _generate_unfinished_issue(item) -> None:
        ...

    def _create_unfinished(self, user: User) -> list:
        ...

    def _create_finished(self, user: User) -> None:
        ...

    def _create_not_started(self) -> None:
        ...
