from django.urls import path

from .views import (
    start_watch_view,
    stop_watch_view,
    volume_authors_list_view,
    volume_characters_list_view,
    volume_concepts_list_view,
    volume_detail_view,
    volume_died_list_view,
    volume_disbanded_list_view,
    volume_download_view,
    volume_first_appearances_list_view,
    volume_issue_detail_view,
    volume_issues_list_view,
    volume_locations_list_view,
    volume_mark_finished_view,
    volume_objects_list_view,
    volume_story_arcs_list_view,
    volume_teams_list_view,
    volumes_list_view,
)

app_name = "volumes"
urlpatterns = [
    path("", view=volumes_list_view, name="list"),
    path("<str:slug>/start_watch/", view=start_watch_view, name="start_watch"),
    path("<str:slug>/stop_watch/", view=stop_watch_view, name="stop_watch"),
    path("<str:slug>/", view=volume_detail_view, name="detail"),
    path("<str:slug>/download/", view=volume_download_view, name="download"),
    path("<str:slug>/mark_finished/", view=volume_mark_finished_view, name="mark_finished"),
    path("<str:slug>/issues/", view=volume_issues_list_view, name="issues_list"),
    path("<str:slug>/characters/", view=volume_characters_list_view, name="characters_list"),
    path("<str:slug>/died/", view=volume_died_list_view, name="died_list"),
    path("<str:slug>/concepts/", view=volume_concepts_list_view, name="concepts_list"),
    path("<str:slug>/locations/", view=volume_locations_list_view, name="locations_list"),
    path("<str:slug>/objects/", view=volume_objects_list_view, name="objects_list"),
    path("<str:slug>/authors/", view=volume_authors_list_view, name="authors_list"),
    path("<str:slug>/story_arcs/", view=volume_story_arcs_list_view, name="story_arcs_list"),
    path("<str:slug>/teams/", view=volume_teams_list_view, name="teams_list"),
    path("<str:slug>/disbanded/", view=volume_disbanded_list_view, name="disbanded_list"),
    path("<str:slug>/first_appearances/", view=volume_first_appearances_list_view, name="first_appearances_list"),
    path("<str:volume_slug>/issues/<str:issue_slug>", view=volume_issue_detail_view, name="issue_detail"),
]
