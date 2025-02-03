from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from read_comics.characters.api.viewsets import CharacterStatsViewSet
from read_comics.concepts.api.viewsets import ConceptStatsViewSet
from read_comics.core.api.viewsets import CoreStatsViewSet
from read_comics.issues.api.viewsets import IssueStatsViewSet
from read_comics.locations.api.viewsets import LocationStatsViewSet
from read_comics.objects.api.viewsets import ObjectStatsViewSet
from read_comics.people.api.viewsets import PersonStatsViewSet
from read_comics.powers.api.viewsets import PowerStatsViewSet
from read_comics.publishers.api.viewsets import PublisherStatsViewSet
from read_comics.story_arcs.api.viewsets import StoryArcStatsViewSet
from read_comics.teams.api.viewsets import TeamStatsViewSet
from read_comics.users.api.views import UserViewSet
from read_comics.volumes.api.viewsets import VolumeStatsViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

router.register("core", CoreStatsViewSet, basename="core")

router.register("characters", CharacterStatsViewSet, basename="character")
router.register("concepts", ConceptStatsViewSet, basename="concept")
router.register("issues", IssueStatsViewSet, basename="issue")
router.register("locations", LocationStatsViewSet, basename="location")
router.register("objects", ObjectStatsViewSet, basename="object")
router.register("people", PersonStatsViewSet, basename="person")
router.register("powers", PowerStatsViewSet, basename="power")
router.register("publishers", PublisherStatsViewSet, basename="publisher")
router.register("story_arcs", StoryArcStatsViewSet, basename="story_arc")
router.register("teams", TeamStatsViewSet, basename="team")
router.register("volumes", VolumeStatsViewSet, basename="volume")

app_name = "api"
urlpatterns = router.urls
