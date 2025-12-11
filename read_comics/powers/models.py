from django.db import models
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker

from read_comics.utils.models import ComicvineSyncModel, slugify_function

from .tasks import power_comicvine_info_task


class Power(ComicvineSyncModel):
    MONGO_COLLECTION = "comicvine_powers"
    MONGO_PROJECTION = {
        "count_of_issue_appearances": 0,
        "date_added": 0,
        "date_last_updated": 0,
        "characters": 0,
    }
    COMICVINE_INFO_TASK = power_comicvine_info_task
    COMICVINE_API_URL = (
        "https://comicvine.gamespot.com/api/power/4035-{id}/?"
        "api_key={api_key}&"
        "format=json&field_list=id,api_detail_url,site_detail_url,name,aliases,description"
    )

    name = models.TextField()
    aliases = models.TextField(null=True)
    html_description = models.TextField(null=True)

    thumb_url = models.URLField(max_length=1000, null=True)
    image_url = models.URLField(max_length=1000, null=True)

    slug = AutoSlugField(
        populate_from=["name"], slugify_function=slugify_function, overwrite=True, max_length=1000, unique=True
    )

    tracker = FieldTracker()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
