import re
from datetime import datetime

import boto3
from django.conf import settings
from django.db import models
from django.utils.encoding import escape_uri_path
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker
from slugify import slugify
from utils.logging import getLogger, methods_logged
from utils.model_mixins import ImageMixin
from utils.models import ComicvineSyncModel, slugify_function

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.issues.tasks import issue_comicvine_info_task
from read_comics.locations.models import Location
from read_comics.missing_issues.models import IgnoredIssue, MissingIssue
from read_comics.objects.models import Object
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume

logger = getLogger(__name__ + ".Issue")


@methods_logged(
    logger,
    methods=[
        "fill_from_comicvine",
        "process_document",
        "get_field_mapping",
        "_fill_field_from_document",
        "_set_non_m2m_from_document",
        "_get_value_by_path",
        "_set_m2m_from_document",
    ],
)
class Issue(ImageMixin, ComicvineSyncModel):
    MONGO_COLLECTION = "comicvine_issues"
    MONGO_PROJECTION = {
        "count_of_issue_appearances": 0,
        "date_added": 0,
        "date_last_updated": 0,
        "first_appearance_characters": 0,
        "first_appearance_concepts": 0,
        "first_appearance_locations": 0,
        "first_appearance_objects": 0,
        "first_appearance_storyarcs": 0,
        "first_appearance_teams": 0,
        "has_staff_review": 0,
    }
    FIELD_MAPPING = {
        "html_description": {"path": "description", "method": "get_description"},
        "number": "issue_number",
        "cover_date": {"path": "cover_date", "method": "convert_date"},
        "store_date": {"path": "store_date", "method": "convert_date"},
        "characters": {"path": "character_credits", "method": "get_character"},
        "characters_died": {"path": "character_died_in", "method": "get_character"},
        "concepts": {"path": "concept_credits", "method": "get_concept"},
        "locations": {"path": "location_credits", "method": "get_location"},
        "objects_in": {"path": "object_credits", "method": "get_object"},
        "people": {"path": "person_credits", "method": "get_author"},
        "story_arcs": {"path": "story_arc_credits", "method": "get_story_arc"},
        "teams": {"path": "team_credits", "method": "get_team"},
        "disbanded_teams": {"path": "team_disbanded_in", "method": "get_team"},
        "volume": {"path": "volume", "method": "get_volume"},
    }
    COMICVINE_INFO_TASK = issue_comicvine_info_task
    COMICVINE_API_URL = (
        "https://comicvine.gamespot.com/api/issue/4000-{id}?"
        "format=json&"
        "field_list=id,api_detail_url,site_detail_url,name,aliases,deck,description,image,"
        "issue_number,cover_date,store_date,character_credits,character_died_in,concept_credits,"
        "location_credits,object_credits,person_credits,story_arc_credits,team_credits,"
        "team_disbanded_in,volume&"
        "api_key={api_key}"
    )

    logger = logger

    name = models.TextField(null=True)
    aliases = models.TextField(null=True)
    short_description = models.TextField(null=True)
    html_description = models.TextField(null=True)
    number = models.CharField(max_length=10, null=True)
    numerical_number = models.FloatField(null=True)

    cover_date = models.DateField(null=True)
    store_date = models.DateField(null=True)

    thumb_url = models.URLField(max_length=1000, null=True)
    image_url = models.URLField(max_length=1000, null=True)

    characters = models.ManyToManyField("characters.Character", related_name="issues")
    characters_died = models.ManyToManyField("characters.Character", related_name="died_in_issues")

    concepts = models.ManyToManyField("concepts.Concept", related_name="issues")

    locations = models.ManyToManyField("locations.Location", related_name="issues")

    objects_in = models.ManyToManyField("objects.Object", related_name="issues")

    people = models.ManyToManyField("people.Person", through="IssuePerson", related_name="issues")

    story_arcs = models.ManyToManyField("story_arcs.StoryArc", related_name="issues")

    teams = models.ManyToManyField("teams.Team", related_name="issues")
    disbanded_teams = models.ManyToManyField("teams.Team", related_name="disbanded_in_issues")

    volume = models.ForeignKey("volumes.Volume", related_name="issues", on_delete=models.CASCADE, null=True)

    finished_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="FinishedIssue", related_name="finished_issues"
    )

    slug = AutoSlugField(
        populate_from=["get_publisher_name", "get_volume_name", "get_volume_start_year", "number", "name"],
        overwrite=True,
        slugify_function=slugify_function,
        max_length=1000,
        unique=True,
    )

    tracker = FieldTracker()

    space_key = models.CharField(max_length=1000)
    size = models.IntegerField(null=True)

    class Meta:
        ordering = ("volume__name", "volume__start_year", "number")

    def __str__(self):
        publisher_name = self.get_publisher_name()
        if publisher_name:
            return f"{self.get_full_name()} ({publisher_name})"
        else:
            return self.get_full_name()

    @staticmethod
    def convert_date(s):
        if s:
            return datetime.fromisoformat(s)
        return None

    @staticmethod
    def get_author(comicvine_author):
        comicvine_id = comicvine_author.get("id")
        name = comicvine_author.get("name", str(comicvine_id))
        role = comicvine_author.get("role")
        from read_comics.people.models import Person

        person, _, _ = Person.objects.get_or_create_from_comicvine(comicvine_id, defaults={"name": name}, delay=True)
        return person, {"role": role}

    # noinspection DuplicatedCode
    def create_links(self):
        Character.objects.filter(first_issue_comicvine_id=self.comicvine_id).update(first_issue=self)
        Concept.objects.filter(first_issue_comicvine_id=self.comicvine_id).update(first_issue=self)
        Location.objects.filter(first_issue_comicvine_id=self.comicvine_id).update(first_issue=self)
        Object.objects.filter(first_issue_comicvine_id=self.comicvine_id).update(first_issue=self)
        StoryArc.objects.filter(first_issue_comicvine_id=self.comicvine_id).update(first_issue=self)
        Team.objects.filter(first_issue_comicvine_id=self.comicvine_id).update(first_issue=self)
        Volume.objects.filter(first_issue_comicvine_id=self.comicvine_id).update(first_issue=self)
        Volume.objects.filter(last_issue_comicvine_id=self.comicvine_id).update(last_issue=self)

    def post_save(self):
        self.create_links()
        MissingIssue.objects.filter(comicvine_id=self.comicvine_id).delete()
        IgnoredIssue.objects.filter(comicvine_id=self.comicvine_id).delete()

    def get_publisher_name(self):
        if self.volume and self.volume.publisher:
            return self.volume.publisher.name
        else:
            return None

    def get_volume_name(self):
        if self.volume:
            return self.volume.name
        else:
            return None

    def get_volume_start_year(self):
        if self.volume:
            return self.volume.start_year
        else:
            return None

    @staticmethod
    def get_description(text):
        description = text
        if description:
            description = re.sub(r"<(a|/a)[^>]*>", "", description)
            description = re.sub(
                r"<h4>List of covers and their creators:<\/h4><table[^>]*>.*?<\/table>", "", description
            )
        return description

    def get_full_name(self, volume_name=None, volume_start_year=None):
        if not self.volume:
            return "unknown"
        if self.name:
            return (
                f"{volume_name or self.volume.name} ({volume_start_year or self.volume.start_year}) "
                f"#{self.number} {self.name}"
            )
        else:
            return f"{volume_name or self.volume.name} ({volume_start_year or self.volume.start_year}) #{self.number}"

    def update_do_metadata(self, volume_name=None, volume_start_year=None):
        filename = f"{self.get_full_name(volume_name, volume_start_year)}.{self.space_key[-3:]}"
        filename_cleaned = slugify(
            filename,
            separator=" ",
            lowercase=False,
            hexadecimal=False,
            regex_pattern=r"[^-a-zA-Z0-9.#*,;]+",
            replacements=(("/", "*"), (":", "*"), ("½", ".5")),
        )
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.DO_SPACE_DATA_KEY,
            aws_secret_access_key=settings.DO_SPACE_DATA_SECRET,
            region_name=settings.DO_SPACE_DATA_REGION,
            endpoint_url=settings.DO_SPACE_DATA_ENDPOINT_URL,
        )
        s3_client.copy_object(
            Bucket=settings.DO_SPACE_DATA_BUCKET,
            Key=self.space_key,
            CopySource={"Bucket": settings.DO_SPACE_DATA_BUCKET, "Key": self.space_key},
            ContentDisposition='attachment; filename="' + filename_cleaned + '"',
            MetadataDirective="REPLACE",
            ACL="public-read",
        )

    def pre_save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.comicvine_status == self.ComicvineStatus.MATCHED:
            if (
                self.tracker.has_changed("number")
                or self.tracker.has_changed("name")
                or self.tracker.has_changed("volume_id")
            ):
                self.update_do_metadata()
            self.set_numerical_number()

    @property
    def download_link(self):
        return escape_uri_path(f"{settings.DO_SPACE_DATA_PUBLIC_URL}/{self.space_key}")

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("issues:detail", args=[self.slug])

    def set_numerical_number(self):
        if self.number:
            if self.number == "½":
                self.numerical_number = 0.5
            else:
                r = re.compile(r"^\d+(\.\d+)?")
                match = r.match(self.number)
                if match:
                    self.numerical_number = float(match.group(0))
                else:
                    self.numerical_number = 0
        else:
            self.numerical_number = None

    @property
    def display_name(self):
        return self.get_full_name()


class IssuePerson(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="authors")
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, related_name="authored_issues")
    role = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return repr(self)


class FinishedIssue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finished")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="finished")
    finish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "issue"),)

    def __str__(self) -> str:
        return repr(self)
