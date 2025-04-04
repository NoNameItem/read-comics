from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker

from read_comics.missing_issues.models import IgnoredIssue, IgnoredPublisher, IgnoredVolume, WatchedItem
from read_comics.utils.model_mixins import ImageMixin
from read_comics.utils.models import ComicvineSyncModel, slugify_function

from .tasks import publisher_comicvine_info_task


class Publisher(ImageMixin, ComicvineSyncModel):
    MONGO_COLLECTION = "comicvine_publishers"
    MONGO_PROJECTION = {
        "count_of_issue_appearances": 0,
        "date_added": 0,
        "date_last_updated": 0,
        "location_address": 0,
        "location_city": 0,
        "story_arcs": 0,
        "volumes": 0,
        "teams": 0,
    }
    COMICVINE_INFO_TASK = publisher_comicvine_info_task
    COMICVINE_API_URL = (
        "https://comicvine.gamespot.com/api/publisher/4010-{id}/?"
        "api_key={api_key}&"
        "format=json&field_list=id,api_detail_url,site_detail_url,name,aliases,deck,description,image"
    )
    COMICVINE_FORCE_DETAIL_INFO = True

    name = models.TextField()
    aliases = models.TextField(null=True)
    short_description = models.TextField(null=True)
    html_description = models.TextField(null=True)

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

    @property
    def http_image_url(self):
        if self.image_url:
            return self.image_url.replace("https:", "http:")
        else:
            return None

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("publishers:detail", args=[self.slug])

    @property
    def download_link(self):
        from django.urls import reverse

        return reverse("publishers:download", args=[self.slug])

    def get_aliases_list(self):
        if self.aliases:
            return self.aliases.split("\n")
        return []

    def post_save(self):
        IgnoredPublisher.objects.filter(comicvine_id=self.comicvine_id).delete()
        IgnoredVolume.objects.filter(publisher_comicvine_id=self.comicvine_id).delete()
        IgnoredIssue.objects.filter(publisher_comicvine_id=self.comicvine_id).delete()
