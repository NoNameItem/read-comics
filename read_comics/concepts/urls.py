from django.urls import path

from .views import (
    concept_detail_view,
    concept_download_view,
    concept_issue_detail_view,
    concept_issues_list_view,
    concept_volumes_list_view,
    concepts_list_view,
    start_watch_view,
    stop_watch_view,
)

app_name = "concepts"
urlpatterns = [
    path("", view=concepts_list_view, name="list"),
    path("<str:slug>/", view=concept_detail_view, name="detail"),
    path("<str:slug>/start_watch/", view=start_watch_view, name="start_watch"),
    path("<str:slug>/stop_watch/", view=stop_watch_view, name="stop_watch"),
    path("<str:slug>/issues/", view=concept_issues_list_view, name="issues"),
    path("<str:slug>/volumes/", view=concept_volumes_list_view, name="volumes"),
    path("<str:concept_slug>/issues/<str:issue_slug>/", view=concept_issue_detail_view, name="issue_detail"),
    path("<str:slug>/download/", view=concept_download_view, name="download"),
]
