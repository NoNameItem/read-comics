from django.urls import path

from .views import (
    character_authors_list_view,
    character_detail_view,
    character_died_in_issues_list_view,
    character_download_view,
    character_enemies_list_view,
    character_friends_list_view,
    character_issue_detail_view,
    character_issues_list_view,
    character_list_view,
    character_team_enemies_list_view,
    character_team_friends_list_view,
    character_teams_list_view,
    character_volumes_list_view,
)

app_name = "characters"
urlpatterns = [
    path("", view=character_list_view, name="list"),
    path("<str:slug>/", view=character_detail_view, name="detail"),
    path("<str:slug>/issues/", view=character_issues_list_view, name="issues"),
    path("<str:slug>/volumes/", view=character_volumes_list_view, name="volumes"),
    path("<str:slug>/died_in_issues/", view=character_died_in_issues_list_view, name="died_in_issues"),
    path("<str:slug>/enemies/", view=character_enemies_list_view, name="enemies"),
    path("<str:slug>/friends/", view=character_friends_list_view, name="friends"),
    path("<str:slug>/teams/", view=character_teams_list_view, name="teams"),
    path("<str:slug>/team_friends/", view=character_team_friends_list_view, name="team_friends"),
    path("<str:slug>/team_enemies/", view=character_team_enemies_list_view, name="team_enemies"),
    path("<str:slug>/authors/", view=character_authors_list_view, name="authors"),
    path("<str:character_slug>/issues/<str:issue_slug>/", view=character_issue_detail_view, name="issue_detail"),
    path("<str:slug>/download/", view=character_download_view, name="download"),
]
