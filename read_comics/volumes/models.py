from django.db import models
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker
from utils.logging import getLogger, methods_logged
from utils.model_mixins import ImageMixin
from utils.models import ComicvineSyncModel, slugify_function
from volumes.tasks import volume_comicvine_info_task

logger = getLogger(__name__ + '.Volume')


@methods_logged(logger, methods=['fill_from_comicvine', 'process_document', 'get_field_mapping',
                                 '_fill_field_from_document', '_set_non_m2m_from_document', '_get_value_by_path',
                                 '_set_m2m_from_document'])
class Volume(ImageMixin, ComicvineSyncModel):
    MONGO_COLLECTION = 'comicvine_volumes'
    MONGO_PROJECTION = {
        'characters': 0,
        'concepts': 0,
        'count_of_issues': 0,
        'date_added': 0,
        'date_last_updated': 0,
        'issue_credits': 0,
        'locations': 0,
        'objects': 0,
        'people': 0
    }
    FIELD_MAPPING = {
        'publisher': {
            'path': 'publisher',
            'method': 'get_publisher'
        },
        'first_issue_name': {
            'path': 'first_issue.id',
            'method': 'get_issue_name'
        },
        'first_issue': {
            'path': 'first_issue.id',
            'method': 'get_issue'
        },
        'first_issue_comicvine_id': 'first_issue.id',
        'last_issue_name': {
            'path': 'last_issue.id',
            'method': 'get_issue_name'
        },
        'last_issue': {
            'path': 'last_issue.id',
            'method': 'get_issue'
        },
        'last_issue_comicvine_id': 'last_issue.id',
        'start_year': 'start_year'
    }
    COMICVINE_INFO_TASK = volume_comicvine_info_task
    COMICVINE_API_URL = 'https://comicvine.gamespot.com/api/volume/4050-{id}/?' \
                        'api_key={api_key}&' \
                        'format=json&' \
                        'field_list=id,api_detail_url,site_detail_url,name,aliases,deck,description,image,' \
                        'first_issue,publisher,last_issue,start_year'

    logger = logger

    name = models.TextField()
    aliases = models.TextField(null=True)
    short_description = models.TextField(null=True)
    html_description = models.TextField(null=True)
    start_year = models.IntegerField(null=True)

    thumb_url = models.URLField(max_length=1000, null=True)
    image_url = models.URLField(max_length=1000, null=True)

    first_issue_name = models.TextField(null=True)
    first_issue = models.ForeignKey('issues.Issue', null=True, on_delete=models.SET_NULL,
                                    related_name='first_issue_of')
    first_issue_comicvine_id = models.IntegerField(null=True)

    last_issue_name = models.TextField(null=True)
    last_issue = models.ForeignKey('issues.Issue', null=True, on_delete=models.SET_NULL,
                                   related_name='last_issue_of')
    last_issue_comicvine_id = models.IntegerField(null=True)

    publisher = models.ForeignKey('publishers.Publisher', related_name='volumes', on_delete=models.CASCADE, null=True)

    slug = AutoSlugField(
        populate_from=[
            "get_publisher_name",
            "name",
            "start_year"
        ],
        slugify_function=slugify_function,
        overwrite=True,
        max_length=1000
    )

    tracker = FieldTracker()

    class Meta:
        ordering = ("name", "start_year",)

    def __str__(self):
        publisher_name = self.get_publisher_name()
        if publisher_name:
            return "%s (%s) (%s)" % (self.name, (self.start_year or ''), publisher_name)
        else:
            return "%s (%s)" % (self.name, (self.start_year or 'Start year unknown'))

    @property
    def full_name(self):
        return "[%s] %s (%s)" % (self.publisher, self.name, self.start_year)

    def get_publisher_name(self):
        if self.publisher:
            return self.publisher.name
        else:
            return None

    def pre_save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from read_comics.issues.models import Issue
        if self.tracker.has_changed('last_issue_comicvine_id'):
            try:
                last_issue = Issue.objects.get(comicvine_id=self.first_issue_comicvine_id)
                self.last_issue = last_issue
            except Issue.DoesNotExist:
                self.last_issue = None
        if self.tracker.has_changed('first_issue_comicvine_id'):
            try:
                first_issue = Issue.objects.get(comicvine_id=self.first_issue_comicvine_id)
                self.first_issue = first_issue
            except Issue.DoesNotExist:
                self.first_issue = None
        if self.tracker.has_changed('name') or self.tracker.has_changed('start_year'):
            self.update_issues_do_metadata()

    def update_issues_do_metadata(self):
        for issue in self.issues.all():
            issue.update_do_metadata(self.name, self.start_year)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('volumes:detail', args=[self.slug])

    @property
    def download_link(self):
        from django.urls import reverse
        return reverse('volumes:download', args=[self.slug])
