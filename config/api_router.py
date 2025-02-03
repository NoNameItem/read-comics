from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from read_comics.characters.api.viewsets import CharacterStatsViewSet
from read_comics.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("characters", CharacterStatsViewSet, basename="character")


app_name = "api"
urlpatterns = router.urls
