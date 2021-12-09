from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
                  path("", include("read_comics.pages.urls", namespace="pages")),
                  # Django Admin, use {% url 'admin:index' %}
                  # path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  path("users/", include("read_comics.users.urls", namespace="users")),
                  path("accounts/", include("allauth.urls")),
                  # Your stuff: custom urls includes go here
                  path("publishers/", include("read_comics.publishers.urls", namespace="publishers")),
                  path("characters/", include("read_comics.characters.urls", namespace="characters")),
                  path("concepts/", include("read_comics.concepts.urls", namespace="concepts")),
                  path("issues/", include("read_comics.issues.urls", namespace="issues")),
                  path("locations/", include("read_comics.locations.urls", namespace="locations")),
                  path("objects/", include("read_comics.objects.urls", namespace="objects")),
                  path("people/", include("read_comics.people.urls", namespace="people")),
                  path("story_arcs/", include("read_comics.story_arcs.urls", namespace="story_arcs")),
                  path("teams/", include("read_comics.teams.urls", namespace="teams")),
                  path("volumes/", include("read_comics.volumes.urls", namespace="volumes")),
                  path("search/", include("read_comics.search.urls", namespace="search")),
                  path("missing_issues/", include("read_comics.missing_issues.urls", namespace="missing_issues")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
