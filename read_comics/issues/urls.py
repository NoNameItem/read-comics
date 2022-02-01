from django.urls import path

from .views import (
    issue_detail_view,
    issue_download_view,
    issue_mark_finished_view,
    issues_list_view,
)

app_name = "issues"
urlpatterns = [
    path("", view=issues_list_view, name="list"),
    path("<str:slug>/", view=issue_detail_view, name="detail"),
    path("<str:slug>/download/", view=issue_download_view, name="download"),
    path("<str:slug>/mark_read/", view=issue_mark_finished_view, name="mark_finished"),
]
