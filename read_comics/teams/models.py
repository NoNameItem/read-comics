from django.db import models
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker
from teams.tasks import team_comicvine_info_task
from utils.logging import getLogger, methods_logged
from utils.model_mixins import ImageMixin
from utils.models import ComicvineSyncModel, slugify_function

logger = getLogger(__name__ + '.Team')


@methods_logged(logger, methods=['fill_from_comicvine', 'process_document', 'get_field_mapping',
                                 '_fill_field_from_document', '_set_non_m2m_from_document', '_get_value_by_path',
                                 '_set_m2m_from_document'])
class Team(ImageMixin, ComicvineSyncModel):
    MONGO_COLLECTION = 'comicvine_teams'
    MONGO_PROJECTION = {
        'character_enemies': 0,
        'character_friends': 0,
        'characters': 0,
        'count_of_issue_appearances': 0,
        'count_of_team_members': 0,
        'date_added': 0,
        'date_last_updated': 0,
        'issue_credits': 0,
        'movies': 0,
        'story_arc_credits': 0,
        'volume_credits': 0
    }
    FIELD_MAPPING = {
        'publisher': {
            'path': 'publisher.id',
            'method': 'get_publisher'
        }
    }
    COMICVINE_INFO_TASK = team_comicvine_info_task
    COMICVINE_API_URL = 'https://comicvine.gamespot.com/api/team/4060-{id}/?' \
                        'api_key={api_key}&' \
                        'format=json&' \
                        'field_list=id,api_detail_url,site_detail_url,name,aliases,deck,description,image,' \
                        'first_appeared_in_issue,publisher'

    logger = logger

    name = models.TextField()
    aliases = models.TextField(null=True)
    short_description = models.TextField(null=True)
    html_description = models.TextField(null=True)

    thumb_url = models.URLField(max_length=1000, null=True)
    image_url = models.URLField(max_length=1000, null=True)

    first_issue_name = models.TextField(null=True)
    first_issue = models.ForeignKey('issues.Issue', null=True, on_delete=models.SET_NULL,
                                    related_name='first_appearance_teams')
    first_issue_comicvine_id = models.IntegerField(null=True)

    publisher = models.ForeignKey('publishers.Publisher', null=True, related_name='teams', on_delete=models.CASCADE)

    slug = AutoSlugField(
        populate_from=[
            "get_publisher_name",
            "name"
        ],
        slugify_function=slugify_function,
        overwrite=True,
        max_length=1000
    )

    tracker = FieldTracker()

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return "%s (%s)" % (self.name, self.publisher)

    def get_publisher_name(self):
        if self.publisher:
            return self.publisher.name
        else:
            return None

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
        return reverse('teams:detail', args=[self.slug])

    def get_aliases_list(self):
        if self.aliases:
            return self.aliases.split('\n')

    @property
    def download_link(self):
        from django.urls import reverse
        return reverse('teams:download', args=[self.slug])
