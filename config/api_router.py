from django.conf import settings
from rest_framework_extensions.routers import ExtendedDefaultRouter as DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


app_name = "api"
urlpatterns = router.urls
