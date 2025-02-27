from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker

from read_comics.missing_issues.models import WatchedItem
from read_comics.utils.model_mixins import ImageMixin
from read_comics.utils.models import ComicvineSyncModel, slugify_function

from .tasks import object_comicvine_info_task


class Object(ImageMixin, ComicvineSyncModel):
    MONGO_COLLECTION = "comicvine_objects"
    MONGO_PROJECTION = {
        "count_of_issue_appearances": 0,
        "date_added": 0,
        "date_last_updated": 0,
        "issue_credits": 0,
        "movies": 0,
        "story_arc_credits": 0,
        "volume_credits": 0,
    }
    FIELD_MAPPING = {"start_year": "start_year"}
    COMICVINE_INFO_TASK = object_comicvine_info_task
    COMICVINE_API_URL = (
        "https://comicvine.gamespot.com/api/object/4055-{id}/?"
        "api_key={api_key}&"
        "format=json&"
        "field_list=id,api_detail_url,site_detail_url,name,aliases,deck,description,image,"
        "first_appeared_in_issue,start_year"
    )

    name = models.TextField()
    aliases = models.TextField(null=True)
    short_description = models.TextField(null=True)
    html_description = models.TextField(null=True)
    start_year = models.IntegerField(null=True)

    first_issue_name = models.TextField(null=True)
    first_issue = models.ForeignKey(
        "issues.Issue", null=True, on_delete=models.SET_NULL, related_name="first_appearance_objects"
    )
    first_issue_comicvine_id = models.IntegerField(null=True)

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

    def pre_save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.tracker.has_changed("first_issue_comicvine_id"):
            from read_comics.issues.models import Issue

            try:
                first_issue = Issue.objects.get(comicvine_id=self.first_issue_comicvine_id)
                self.first_issue = first_issue
            except Issue.DoesNotExist:
                self.first_issue = None

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("objects:detail", args=[self.slug])

    @property
    def download_link(self):
        from django.urls import reverse

        return reverse("objects:download", args=[self.slug])

    def get_aliases_list(self):
        if self.aliases:
            return self.aliases.split("\n")
        return []
