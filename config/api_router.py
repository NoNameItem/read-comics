from django.conf import settings
from rest_framework_extensions.routers import ExtendedDefaultRouter as DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter

from read_comics.characters.api.viewsets import CharacterViewSet
from read_comics.concepts.api.viewsets import ConceptViewSet
from read_comics.issues.api.viewsets import IssueViewSet
from read_comics.locations.api.viewsets import LocationViewSet
from read_comics.missing_issues.api.viewsets import MissingIssueViewSet
from read_comics.objects.api.viewsets import ObjectViewSet
from read_comics.people.api.viewsets import PeopleViewSet
from read_comics.publishers.api.viewsets import PublishersViewSet
from read_comics.story_arcs.api.viewsets import StoryArcsViewSet
from read_comics.teams.api.viewsets import TeamsViewSet
from read_comics.volumes.api.viewsets import VolumesViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"

# Character urls
character_router = router.register("characters", CharacterViewSet, basename="character")

# Concept urls
concept_router = router.register("concepts", ConceptViewSet, basename="concept")

# Issue urls
issue_router = router.register("issues", IssueViewSet, basename="issue")

# Location urls
location_router = router.register("locations", LocationViewSet, basename="location")

# Missing issue urls
missing_issue_router = router.register("missing-issues", MissingIssueViewSet, basename="missing-issue")

# Object urls
object_router = router.register("objects", ObjectViewSet, basename="object")

# People urls
people_router = router.register("people", PeopleViewSet, basename="people")

# People urls
publisher_router = router.register("publishers", PublishersViewSet, basename="publisher")

# Story arc urls
story_arc_router = router.register("story-arcs", StoryArcsViewSet, basename="story-arc")

# team urls
team_router = router.register("teams", TeamsViewSet, basename="team")

# volume urls
volume_router = router.register("volumes", VolumesViewSet, basename="volume")

urlpatterns = router.urls
