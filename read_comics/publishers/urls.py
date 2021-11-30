from django.urls import path

from .views import (
    publisher_characters_list_view,
    publisher_detail_view,
    publisher_download_view,
    publisher_issue_detail_view,
    publisher_issues_list_view,
    publisher_list_view,
    publisher_story_arcs_list_view,
    publisher_teams_list_view,
    publisher_volumes_list_view,
)

app_name = "publishers"
urlpatterns = [
    path("", view=publisher_list_view, name="list"),
    path("<str:slug>/", view=publisher_detail_view, name="detail"),
    path("<str:slug>/issues/", view=publisher_issues_list_view, name="issues"),
    path("<str:slug>/characters/", view=publisher_characters_list_view, name="characters"),
    path("<str:slug>/teams/", view=publisher_teams_list_view, name="teams"),
    path("<str:slug>/story_arcs/", view=publisher_story_arcs_list_view, name="story_arcs"),
    path("<str:slug>/volumes/", view=publisher_volumes_list_view, name="volumes"),
    path("<str:slug>/download/", view=publisher_download_view, name="download"),
    path("<str:publisher_slug>/issues/<str:issue_slug>/", view=publisher_issue_detail_view, name="issue_detail"),
]
