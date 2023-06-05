# pylint: skip-file

from typing import Protocol


class APIUrlTest(Protocol):
    base_name: str
    base_url: str
