from typing import Protocol

from django.db.models import QuerySet, Sum
from django.template.defaultfilters import filesizeformat


class ImageMixin:
    image_url: str
    thumb_url: str

    @property
    def full_size_url(self):
        if self.image_url:
            return self.image_url
        else:
            return None

    @property
    def thumb_size_url(self):
        if self.thumb_url:
            return self.thumb_url  # .replace("https:", "http:")
        else:
            return None

    def get_image_size(self, size):
        url = self.thumb_size_url
        if url:
            return url.replace("/scale_small/", "/" + size + "/")
        return url

    @property
    def square_avatar(self):
        # 80x80
        return self.get_image_size("square_avatar")

    @property
    def square_tiny(self):
        # 160x160
        return self.get_image_size("square_tiny")

    @property
    def square_small(self):
        # 320x320
        return self.get_image_size("square_small")

    @property
    def square_medium(self):
        # 480x480
        return self.get_image_size("square_medium")


class HasIssuesProtocol(Protocol):
    issues: QuerySet


class DownloadSizeMixin:
    @property
    def download_size(self: HasIssuesProtocol) -> str:
        return filesizeformat(self.issues.filter(comicvine_status="MATCHED").aggregate(v=Sum("size"))["v"])


class HasAliasesProtocol(Protocol):
    aliases: str


class AliasesListMixin:
    def get_aliases_list(self: HasAliasesProtocol) -> list[str]:
        if self.aliases:
            return self.aliases.split("\n")
        return []
