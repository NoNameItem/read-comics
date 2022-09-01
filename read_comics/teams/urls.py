from django.urls import path

from .views import (
    start_watch_view,
    stop_watch_view,
    team_characters_list_view,
    team_detail_view,
    team_disbanded_in_issues_list_view,
    team_download_view,
    team_enemies_list_view,
    team_friends_list_view,
    team_issue_detail_view,
    team_issues_list_view,
    team_volumes_list_view,
    teams_list_view,
)

app_name = "teams"
urlpatterns = [
    path("", view=teams_list_view, name="list"),
    path("<str:slug>/", view=team_detail_view, name="detail"),
    path("<str:slug>/start_watch/", view=start_watch_view, name="start_watch"),
    path("<str:slug>/stop_watch/", view=stop_watch_view, name="stop_watch"),
    path("<str:slug>/download/", view=team_download_view, name="download"),
    path("<str:team_slug>/issues/<issue_slug>/", view=team_issue_detail_view, name="issue_detail"),
    path("<str:slug>/issues/", view=team_issues_list_view, name="issues_list"),
    path("<str:slug>/enemies/", view=team_enemies_list_view, name="enemies_list"),
    path("<str:slug>/volumes/", view=team_volumes_list_view, name="volumes_list"),
    path("<str:slug>/friends/", view=team_friends_list_view, name="friends_list"),
    path("<str:slug>/characters/", view=team_characters_list_view, name="characters_list"),
    path("<str:slug>/disbanded_in/", view=team_disbanded_in_issues_list_view, name="disbanded_in_issues_list"),
]
