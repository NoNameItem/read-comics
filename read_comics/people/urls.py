from django.urls import path

from .views import (
    people_list_view,
    person_characters_list_view,
    person_detail_view,
    person_download_view,
    person_issue_detail_view,
    person_issues_list_view,
    person_volumes_list_view,
    start_watch_view,
    stop_watch_view,
)

app_name = "people"
urlpatterns = [
    path("", view=people_list_view, name="list"),
    path("<str:slug>/", view=person_detail_view, name="detail"),
    path("<str:slug>/start_watch/", view=start_watch_view, name="start_watch"),
    path("<str:slug>/stop_watch/", view=stop_watch_view, name="stop_watch"),
    path("<str:slug>/issues/", view=person_issues_list_view, name="issues"),
    path("<str:slug>/volumes/", view=person_volumes_list_view, name="volumes"),
    path("<str:slug>/characters/", view=person_characters_list_view, name="characters"),
    path("<str:person_slug>/issues/<str:issue_slug>/", view=person_issue_detail_view, name="issue_detail"),
    path("<str:slug>/download/", view=person_download_view, name="download"),
]
