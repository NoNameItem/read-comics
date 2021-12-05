from datetime import datetime

from characters.tasks import character_comicvine_info_task
from django.db import models
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker
from utils.logging import getLogger, methods_logged
from utils.model_mixins import ImageMixin
from utils.models import ComicvineSyncModel, slugify_function

logger = getLogger(__name__ + '.Character')


@methods_logged(logger, methods=['fill_from_comicvine', 'process_document', 'get_field_mapping',
                                 '_fill_field_from_document', '_set_non_m2m_from_document', '_get_value_by_path',
                                 '_set_m2m_from_document'])
class Character(ImageMixin, ComicvineSyncModel):
    class Gender(models.IntegerChoices):
        OTHER = 0, 'Other'
        MALE = 1, 'Male'
        FEMALE = 2, 'Female'

    MONGO_COLLECTION = 'comicvine_characters'
    MONGO_PROJECTION = {
        'count_of_issue_appearances': 0,
        'date_added': 0,
        'date_last_updated': 0,
        'issue_credits': 0,
        'issues_died_in': 0,
        'movies': 0,
        'story_arc_credits': 0,
        'volume_credits': 0,

    }
    FIELD_MAPPING = {
        'real_name': 'real_name',
        'gender': 'gender',
        'birth': {
            'path': 'birth',
            'method': 'convert_date'
        },
        'origin': 'origin.name',
        'character_enemies': {
            'path': 'character_enemies',
            'method': 'get_character'
        },
        'character_friends': {
            'path': 'character_friends',
            'method': 'get_character'
        },
        'teams': {
            'path': 'teams',
            'method': 'get_team'
        },
        'team_enemies': {
            'path': 'team_enemies',
            'method': 'get_team'
        },
        'team_friends': {
            'path': 'team_friends',
            'method': 'get_team'
        },
        'publisher': {
            'path': 'publisher',
            'method': 'get_publisher'
        },
        'creators': {
            'path': 'creators',
            'method': 'get_person'
        },
        'powers': {
            'path': 'powers',
            'method': 'get_power'
        },
    }
    COMICVINE_INFO_TASK = character_comicvine_info_task
    COMICVINE_API_URL = 'https://comicvine.gamespot.com/api/character/4005-{id}/?' \
                        'api_key={api_key}&' \
                        'format=json&' \
                        'field_list=id,api_detail_url,site_detail_url,name,aliases,deck,description,image,' \
                        'first_appeared_in_issue,real_name,gender,birth,origin,character_friends,character_enemies,' \
                        'teams,team_enemies,team_friends,publisher,creators,powers'

    logger = logger

    name = models.TextField(null=True)
    real_name = models.TextField(null=True)
    aliases = models.TextField(null=True)
    short_description = models.TextField(null=True)
    html_description = models.TextField(null=True)
    gender = models.IntegerField(choices=Gender.choices, null=True)
    birth = models.DateField(null=True)
    origin = models.TextField(null=True)

    thumb_url = models.URLField(max_length=1000, null=True)
    image_url = models.URLField(max_length=1000, null=True)

    publisher = models.ForeignKey('publishers.Publisher', null=True, on_delete=models.CASCADE,
                                  related_name='characters')

    character_enemies = models.ManyToManyField('self')
    character_friends = models.ManyToManyField('self')

    teams = models.ManyToManyField('teams.Team', related_name='characters')
    team_enemies = models.ManyToManyField('teams.Team', related_name='character_enemies')
    team_friends = models.ManyToManyField('teams.Team', related_name='character_friends')

    first_issue_name = models.TextField(null=True)
    first_issue = models.ForeignKey('issues.Issue', null=True, on_delete=models.SET_NULL,
                                    related_name='first_appearance_characters')
    first_issue_comicvine_id = models.IntegerField(null=True)

    creators = models.ManyToManyField('people.Person', related_name='created_characters')

    powers = models.ManyToManyField('powers.Power', related_name='characters')

    slug = AutoSlugField(
        populate_from=[
            'get_publisher_name',
            'name'
        ],
        slugify_function=slugify_function,
        overwrite=True,
        max_length=1000
    )

    tracker = FieldTracker()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        if self.get_publisher_name():
            return f"{self.name} ({self.publisher.name})"
        return self.name

    def get_publisher_name(self):
        if self.publisher:
            return self.publisher.name
        else:
            return None

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('characters:detail', args=[self.slug])

    @staticmethod
    def convert_date(s):
        if s:
            return datetime.strptime(s, '%b %d, %Y')
        return None

    def pre_save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.tracker.has_changed('first_issue_comicvine_id'):
            from read_comics.issues.models import Issue
            try:
                first_issue = Issue.objects.get(comicvine_id=self.first_issue_comicvine_id)
                self.first_issue = first_issue
            except Issue.DoesNotExist:
                self.first_issue = None

    def get_aliases_list(self):
        if self.aliases:
            return self.aliases.split('\n')

    @property
    def download_link(self):
        from django.urls import reverse
        return reverse('characters:download', args=[self.slug])
