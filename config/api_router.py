from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from read_comics.characters.api.viewsets import CharacterStatsViewSet
from read_comics.concepts.api.viewsets import ConceptStatsViewSet
from read_comics.issues.api.viewsets import IssueStatsViewSet
from read_comics.locations.api.viewsets import LocationStatsViewSet
from read_comics.objects.api.viewsets import ObjectStatsViewSet
from read_comics.people.api.viewsets import PersonStatsViewSet
from read_comics.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

router.register("characters", CharacterStatsViewSet, basename="character")
router.register("concepts", ConceptStatsViewSet, basename="concept")
router.register("issues", IssueStatsViewSet, basename="issue")
router.register("locations", LocationStatsViewSet, basename="location")
router.register("objects", ObjectStatsViewSet, basename="object")
router.register("people", PersonStatsViewSet, basename="person")


app_name = "api"
urlpatterns = router.urls
