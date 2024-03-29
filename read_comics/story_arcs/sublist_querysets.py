from django.db.models import Count, F, Q, TextField, Value
from django.db.models.functions import Concat, Replace

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.issues.view_mixins import IssuesSublistQueryset
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.teams.models import Team
from read_comics.volumes.view_mixins import VolumesSublistQueryset


class StoryArcSublistQuerysets(IssuesSublistQueryset, VolumesSublistQueryset):
    @staticmethod
    def get_characters_queryset(story_arc):
        return (
            Character.objects.filter(issues__in=story_arc.issues.all())
            .annotate(
                issues_count=Count("issues", filter=Q(issues__in=story_arc.issues.all())),
                desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField()),
            )
            .order_by("-issues_count", "name", "id")
        )

    @staticmethod
    def get_died_queryset(story_arc):
        return Character.objects.filter(died_in_issues__in=story_arc.issues.all()).distinct().order_by("name", "id")

    @staticmethod
    def get_concepts_queryset(story_arc):
        return (
            Concept.objects.filter(issues__in=story_arc.issues.all())
            .annotate(
                issues_count=Count("issues", filter=Q(issues__in=story_arc.issues.all())),
                desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField()),
            )
            .order_by("-issues_count", "name", "id")
        )

    @staticmethod
    def get_locations_queryset(story_arc):
        return (
            Location.objects.filter(issues__in=story_arc.issues.all())
            .annotate(
                issues_count=Count("issues", filter=Q(issues__in=story_arc.issues.all())),
                desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField()),
            )
            .order_by("-issues_count", "name", "id")
        )

    @staticmethod
    def get_objects_queryset(story_arc):
        return (
            Object.objects.filter(issues__in=story_arc.issues.all())
            .annotate(
                issues_count=Count("issues", filter=Q(issues__in=story_arc.issues.all())),
                desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField()),
            )
            .order_by("-issues_count", "name", "id")
        )

    @staticmethod
    def get_authors_queryset(story_arc):
        return (
            Person.objects.filter(issues__in=story_arc.issues.all())
            .annotate(
                issues_count=Count("issues", filter=Q(issues__in=story_arc.issues.all())),
                desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField()),
            )
            .order_by("-issues_count", "name", "id")
        )

    @staticmethod
    def get_teams_queryset(story_arc):
        return (
            Team.objects.filter(issues__in=story_arc.issues.all())
            .annotate(
                issues_count=Count("issues", filter=Q(issues__in=story_arc.issues.all())),
                desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField()),
            )
            .order_by("-issues_count", "name", "id")
        )

    @staticmethod
    def get_disbanded_queryset(story_arc):
        return Team.objects.filter(issues__in=story_arc.issues.all()).distinct().order_by("name", "id")

    @staticmethod
    def get_first_appearance_queryset(story_arc):
        def get_subquery(model, url_template_name, heading):
            return model.objects.filter(first_issue__in=story_arc.issues.all()).values(
                "name",
                "slug",
                url_template_name=Value(url_template_name),
                group_breaker=Value(heading),
                desc=Concat(Value("In issue #"), F("first_issue__number"), output_field=TextField()),
                square_avatar=Replace(
                    Replace("thumb_url", Value("https:"), Value("http:")),
                    Value("/scale_small/"),
                    Value("/square_avatar/"),
                ),
            )

        characters = get_subquery(Character, "characters/detail_url.html", "Characters first appearance")
        concepts = get_subquery(Concept, "concepts/detail_url.html", "Concepts first appearance")
        locations = get_subquery(Location, "locations/detail_url.html", "Locations first appearance")
        objects = get_subquery(Object, "objects/detail_url.html", "Objects first appearance")
        teams = get_subquery(Team, "teams/detail_url.html", "Teams first appearance")

        return characters.union(concepts, locations, objects, teams).order_by("group_breaker", "name")
