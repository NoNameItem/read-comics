from django.db.models import Count, F, Q, TextField, Value
from django.db.models.functions import Concat, Replace

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team


def get_issues_queryset(volume, user=None):
    q = volume.issues.filter(comicvine_status="MATCHED").order_by("numerical_number", "number").annotate(
        parent_slug=F("volume__slug"),
        badge_name=Concat(
            Value("#"), F("number"), Value(" "), F("name"), output_field=TextField()
        ),
        desc=F("cover_date")
    )
    if user and user.is_authenticated:
        return q.annotate(finished_flg=Count("finished_users", distinct=True, filter=Q(finished_users=user)))
    return q


def get_characters_queryset(volume):
    return Character.objects.filter(comicvine_status="MATCHED").filter(issues__volume=volume).annotate(
        issues_count=Count("issues", filter=Q(issues__volume=volume)),
        desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField())
    ).order_by("-issues_count", "name", "id")


def get_died_queryset(volume):
    return Character.objects.filter(comicvine_status="MATCHED").filter(died_in_issues__volume=volume).distinct().\
        order_by("name", "id")


def get_concepts_queryset(volume):
    return Concept.objects.filter(comicvine_status="MATCHED").filter(issues__volume=volume).annotate(
        issues_count=Count("issues", filter=Q(issues__volume=volume)),
        desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField())
    ).order_by("-issues_count", "name", "id")


def get_locations_queryset(volume):
    return Location.objects.filter(comicvine_status="MATCHED").filter(issues__volume=volume).annotate(
        issues_count=Count("issues", filter=Q(issues__volume=volume)),
        desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField())
    ).order_by("-issues_count", "name", "id")


def get_objects_queryset(volume):
    return Object.objects.filter(comicvine_status="MATCHED").filter(issues__volume=volume).annotate(
        issues_count=Count("issues", filter=Q(issues__volume=volume)),
        desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField())
    ).order_by("-issues_count", "name", "id")


def get_authors_queryset(volume):
    return Person.objects.filter(comicvine_status="MATCHED").filter(issues__volume=volume).annotate(
        issues_count=Count("issues", filter=Q(issues__volume=volume)),
        desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField())
    ).order_by("-issues_count", "name", "id")


def get_story_arcs_queryset(volume):
    return StoryArc.objects.filter(comicvine_status="MATCHED").filter(issues__volume=volume).distinct().\
        order_by("name", "id")


def get_teams_queryset(volume):
    return Team.objects.filter(comicvine_status="MATCHED").filter(issues__volume=volume).annotate(
        issues_count=Count("issues", filter=Q(issues__volume=volume)),
        desc=Concat(Value("Appeared in "), F("issues_count"), Value(" issue(s)"), output_field=TextField())
    ).order_by("-issues_count", "name", "id")


def get_disbanded_queryset(volume):
    return Team.objects.filter(comicvine_status="MATCHED").filter(disbanded_in_issues__volume=volume).distinct().\
        order_by("name", "id")


def get_first_appearance_queryset(volume):
    def get_subquery(model, url_template_name, heading):
        return model.objects.filter(comicvine_status="MATCHED").filter(first_issue__volume=volume).values(
            "name", "slug",
            url_template_name=Value(url_template_name),
            group_breaker=Value(heading),
            desc=Concat(Value("In issue #"), F("first_issue__number"), output_field=TextField()),
            square_avatar=Replace(
                Replace("thumb_url", Value("https:"), Value("http:")), Value("/scale_small/"), Value("/square_avatar/")
            )
        )

    characters = get_subquery(Character, "characters/detail_url.html", "Characters first appearance")
    concepts = get_subquery(Concept, "concepts/detail_url.html", "Concepts first appearance")
    locations = get_subquery(Location, "locations/detail_url.html", "Locations first appearance")
    objects = get_subquery(Object, "objects/detail_url.html", "Objects first appearance")
    teams = get_subquery(Team, "teams/detail_url.html", "Teams first appearance")

    return characters.union(concepts, locations, objects, teams).order_by("group_breaker", "name")
