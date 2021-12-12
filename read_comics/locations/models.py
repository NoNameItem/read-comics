from django.db import models
from django_extensions.db.fields import AutoSlugField
from locations.tasks import location_comicvine_info_task
from model_utils import FieldTracker
from utils.logging import getLogger, methods_logged
from utils.model_mixins import ImageMixin
from utils.models import ComicvineSyncModel, slugify_function

logger = getLogger(__name__ + '.Location')


@methods_logged(logger, methods=['fill_from_comicvine', 'process_document', 'get_field_mapping',
                                 '_fill_field_from_document', '_set_non_m2m_from_document', '_get_value_by_path',
                                 '_set_m2m_from_document'])
class Location(ImageMixin, ComicvineSyncModel):
    MONGO_COLLECTION = 'comicvine_locations'
    MONGO_PROJECTION = {
        'count_of_issue_appearances': 0,
        'date_added': 0,
        'date_last_updated': 0,
        'issue_credits': 0,
        'movies': 0,
        'story_arc_credits': 0,
        'volume_credits': 0
    }
    FIELD_MAPPING = {
        'start_year': 'start_year'
    }
    COMICVINE_INFO_TASK = location_comicvine_info_task
    COMICVINE_API_URL = 'https://comicvine.gamespot.com/api/location/4020-{id}/?' \
                        'api_key={api_key}&' \
                        'format=json&' \
                        'field_list=id,api_detail_url,site_detail_url,name,aliases,deck,description,image,' \
                        'first_appeared_in_issue,start_year'

    logger = logger

    name = models.TextField()
    aliases = models.TextField(null=True)
    short_description = models.TextField(null=True)
    html_description = models.TextField(null=True)
    start_year = models.IntegerField(null=True)

    first_issue_name = models.TextField(null=True)
    first_issue = models.ForeignKey('issues.Issue', null=True, on_delete=models.SET_NULL,
                                    related_name='first_appearance_locations')
    first_issue_comicvine_id = models.IntegerField(null=True)

    thumb_url = models.URLField(max_length=1000, null=True)
    image_url = models.URLField(max_length=1000, null=True)

    slug = AutoSlugField(populate_from=["name"], slugify_function=slugify_function, overwrite=True,
                         max_length=1000,
                         unique=True)

    tracker = FieldTracker()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def pre_save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.tracker.has_changed('first_issue_comicvine_id'):
            from read_comics.issues.models import Issue
            try:
                first_issue = Issue.objects.get(comicvine_id=self.first_issue_comicvine_id)
                self.first_issue = first_issue
            except Issue.DoesNotExist:
                self.first_issue = None

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('locations:detail', args=[self.slug])

    @property
    def download_link(self):
        from django.urls import reverse
        return reverse('locations:download', args=[self.slug])

    def get_aliases_list(self):
        if self.aliases:
            return self.aliases.split('\n')
