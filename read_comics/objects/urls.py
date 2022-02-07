from django.urls import path

from .views import (
    object_detail_view,
    object_download_view,
    object_issue_detail_view,
    object_issues_list_view,
    object_volumes_list_view,
    objects_list_view,
    start_watch_view,
    stop_watch_view,
)

app_name = "objects"
urlpatterns = [
    path("", view=objects_list_view, name="list"),
    path("<str:slug>/", view=object_detail_view, name="detail"),
    path("<str:slug>/start_watch/", view=start_watch_view, name="start_watch"),
    path("<str:slug>/stop_watch/", view=stop_watch_view, name="stop_watch"),
    path("<str:slug>/issues/", view=object_issues_list_view, name="issues"),
    path("<str:slug>/volumes/", view=object_volumes_list_view, name="volumes"),
    path("<str:object_slug>/issues/<str:issue_slug>/", view=object_issue_detail_view, name="issue_detail"),
    path("<str:slug>/download/", view=object_download_view, name="download"),
]
