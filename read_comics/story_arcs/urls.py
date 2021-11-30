from django.urls import path

from .views import (
    story_arc_authors_list_view,
    story_arc_characters_list_view,
    story_arc_concepts_list_view,
    story_arc_detail_view,
    story_arc_died_list_view,
    story_arc_disbanded_list_view,
    story_arc_download_view,
    story_arc_first_appearances_list_view,
    story_arc_issue_detail_view,
    story_arc_issues_list_view,
    story_arc_locations_list_view,
    story_arc_mark_finished_view,
    story_arc_objects_list_view,
    story_arc_teams_list_view,
    story_arc_volumes_list_view,
    story_arcs_list_view,
)

app_name = "story_arcs"
urlpatterns = [
    path("", view=story_arcs_list_view, name="list"),
    path("<str:slug>/", view=story_arc_detail_view, name="detail"),
    path("<str:slug>/mark_finished/", view=story_arc_mark_finished_view, name="mark_finished"),
    path("<str:slug>/download/", view=story_arc_download_view, name="download"),
    path("<str:slug>/died/", view=story_arc_died_list_view, name="died"),
    path("<str:slug>/authors/", view=story_arc_authors_list_view, name="authors"),
    path("<str:slug>/characters/", view=story_arc_characters_list_view, name="characters"),
    path("<str:slug>/concepts/", view=story_arc_concepts_list_view, name="concepts"),
    path("<str:slug>/disbanded/", view=story_arc_disbanded_list_view, name="disbanded"),
    path("<str:slug>/first_appearances/", view=story_arc_first_appearances_list_view, name="first_appearances"),
    path("<str:story_arc_slug>/issues/<str:issue_slug>/", view=story_arc_issue_detail_view, name="issue_detail"),
    path("<str:slug>/locations/", view=story_arc_locations_list_view, name="locations"),
    path("<str:slug>/issues/", view=story_arc_issues_list_view, name="issues"),
    path("<str:slug>/objects/", view=story_arc_objects_list_view, name="objects"),
    path("<str:slug>/teams/", view=story_arc_teams_list_view, name="teams"),
    path("<str:slug>/volumes/", view=story_arc_volumes_list_view, name="volumes"),
]
