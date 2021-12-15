from django.urls import path

from .views import (
    location_detail_view,
    location_download_view,
    location_issue_detail_view,
    location_issues_list_view,
    location_volumes_list_view,
    locations_list_view,
    start_watch_view,
    stop_watch_view,
)

app_name = "locations"
urlpatterns = [
    path("", view=locations_list_view, name="list"),
    path("<str:slug>/", view=location_detail_view, name="detail"),
    path("<str:slug>/start_watch/", view=start_watch_view, name="start_watch"),
    path("<str:slug>/stop_watch/", view=stop_watch_view, name="stop_watch"),
    path("<str:slug>/issues/", view=location_issues_list_view, name="issues"),
    path("<str:slug>/volumes/", view=location_volumes_list_view, name="volumes"),
    path("<str:location_slug>/issues<str:issue_slug>/", view=location_issue_detail_view, name="issue_detail"),
    path("<str:slug>/download/", view=location_download_view, name="download"),
]
