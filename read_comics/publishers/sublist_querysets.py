from django.db.models import Count, F, Q, TextField, Value
from django.db.models.functions import Concat

from read_comics.characters.models import Character
from read_comics.issues.models import Issue
from read_comics.issues.view_mixins import IssuesSublistQueryset
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume
from read_comics.volumes.view_mixins import VolumesSublistQueryset


class PublisherSublistQuerysets(IssuesSublistQueryset, VolumesSublistQueryset):
    @staticmethod
    def _get_issues_sublist(obj):
        return Issue.objects.filter(comicvine_status="MATCHED").filter(volume__publisher=obj)

    @staticmethod
    def _get_volumes_sublist(obj):
        return Volume.objects.filter(publisher=obj).filter(comicvine_status="MATCHED")

    @staticmethod
    def get_characters_queryset(publisher):
        return (
            Character.objects.filter(publisher=publisher)
            .annotate(
                issues_count=Count("issues", filter=Q(issues__volume__publisher=publisher)),
                desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField()),
            )
            .order_by("-issues_count", "name", "id")
        )

    @staticmethod
    def get_story_arcs_queryset(publisher):
        return StoryArc.objects.filter(publisher=publisher).distinct().order_by("name", "id")

    @staticmethod
    def get_teams_queryset(publisher):
        return (
            Team.objects.filter(publisher=publisher)
            .annotate(
                issues_count=Count("issues", filter=Q(issues__volume__publisher=publisher)),
                desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField()),
            )
            .order_by("-issues_count", "name", "id")
        )
