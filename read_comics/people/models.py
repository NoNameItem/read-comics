from datetime import datetime

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker

from read_comics.missing_issues.models import WatchedItem
from read_comics.utils.model_mixins import ImageMixin
from read_comics.utils.models import ComicvineSyncModel, slugify_function

from .tasks import person_comicvine_info_task


class Person(ImageMixin, ComicvineSyncModel):
    MONGO_COLLECTION = "comicvine_people"
    MONGO_PROJECTION = {
        "count_of_issue_appearances": 0,
        "date_added": 0,
        "date_last_updated": 0,
        "issues": 0,
        "story_arc_credits": 0,
        "volume_credits": 0,
        "created_characters": 0,
        "email": 0,
        "gender": 0,
    }
    FIELD_MAPPING = {
        "birth_date": {"path": "birth", "method": "convert_date"},
        "country": "country",
        "death_date": {"path": "death.date", "method": "convert_date"},
        "hometown": "hometown",
    }
    COMICVINE_INFO_TASK = person_comicvine_info_task
    COMICVINE_API_URL = (
        "https://comicvine.gamespot.com/api/person/4040-{id}/?"
        "api_key={api_key}&"
        "format=json&field_list=id,api_detail_url,site_detail_url,name,aliases,deck,description,"
        "image,birth,country,death,hometown"
    )

    name = models.TextField(null=True)
    aliases = models.TextField(null=True)
    short_description = models.TextField(null=True)
    html_description = models.TextField(null=True)

    birth_date = models.DateField(null=True)
    death_date = models.DateField(null=True)

    hometown = models.TextField(null=True)
    country = models.TextField(null=True)

    thumb_url = models.URLField(max_length=1000, null=True)
    image_url = models.URLField(max_length=1000, null=True)

    slug = AutoSlugField(
        populate_from=["name"], slugify_function=slugify_function, overwrite=True, max_length=1000, unique=True
    )

    watchers = GenericRelation(WatchedItem)

    tracker = FieldTracker()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    @staticmethod
    def convert_date(s):
        if s:
            return datetime.fromisoformat(s)
        return None

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("people:detail", args=[self.slug])

    @property
    def download_link(self):
        from django.urls import reverse

        return reverse("people:download", args=[self.slug])

    def get_aliases_list(self):
        if self.aliases:
            return self.aliases.split("\n")
        return []
