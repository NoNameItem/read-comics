from django.urls import path

from .views import (
    do_space_view,
    ignore_issue_view,
    ignore_publisher_view,
    ignore_volume_view,
    ignored_issue_delete_view,
    ignored_issues_list_view,
    ignored_publisher_delete_view,
    ignored_publishers_list_view,
    ignored_volume_delete_view,
    ignored_volumes_list_view,
    missing_issues_list_view,
    purge_deleted_from_do_view,
    skip_issue_view,
    skip_publisher_view,
    skip_volume_view,
    start_reload_from_do_view,
    watched_ignore_issue_view,
    watched_ignore_publisher_view,
    watched_ignore_volume_view,
    watched_missing_issues_list_view,
    watched_skip_issue_view,
    watched_skip_publisher_view,
    watched_skip_volume_view,
)

app_name = "missing_issues"

urlpatterns = [
    path("", view=missing_issues_list_view, name="all"),

    path("do_space/", view=do_space_view, name="do_space"),
    path("purge_deleted/", view=purge_deleted_from_do_view, name="purge_deleted"),

    path("ignored_issues/", view=ignored_issues_list_view, name="ignored_issues"),
    path("ignored_volumes/", view=ignored_volumes_list_view, name="ignored_volumes"),
    path("ignored_publishers/", view=ignored_publishers_list_view, name="ignored_publisher"),

    path("ignored_issues/<int:pk>/delete/", view=ignored_issue_delete_view, name="delete_ignored_issue"),
    path("ignored_volumes/<int:pk>/delete/", view=ignored_volume_delete_view, name="delete_ignored_volume"),
    path("ignored_publishers/<int:pk>/delete/", view=ignored_publisher_delete_view, name="delete_ignored_publisher"),

    path("skip_issue/<int:comicvine_id>/", view=skip_issue_view, name="skip_issue"),
    path("skip_volume/<int:comicvine_id>/", view=skip_volume_view, name="skip_volume"),
    path("skip_publisher/<int:comicvine_id>/", view=skip_publisher_view, name="skip_publisher"),

    path("ignore_issue/<int:comicvine_id>/", view=ignore_issue_view, name="ignore_issue"),
    path("ignore_volume/<int:comicvine_id>/", view=ignore_volume_view, name="ignore_volume"),
    path("ignore_publisher/<int:comicvine_id>/", view=ignore_publisher_view, name="ignore_publisher"),

    path("reload_from_do/", view=start_reload_from_do_view, name="start_reload_from_do"),

    path("watched/", view=watched_missing_issues_list_view, name="watched"),

    path("watched/skip_issue/<int:comicvine_id>/", view=watched_skip_issue_view, name="watched_skip_issue"),
    path("watched/skip_volume/<int:comicvine_id>/", view=watched_skip_volume_view, name="watched_skip_volume"),
    path("watched/skip_publisher/<int:comicvine_id>/", view=watched_skip_publisher_view, name="watched_skip_publisher"),

    path("watched/ignore_issue/<int:comicvine_id>/", view=watched_ignore_issue_view, name="watched_ignore_issue"),
    path("watched/ignore_volume/<int:comicvine_id>/", view=watched_ignore_volume_view, name="watched_ignore_volume"),
    path("watched/ignore_publisher/<int:comicvine_id>/", view=watched_ignore_publisher_view,
         name="watched_ignore_publisher"),

    path("<str:category>/<str:slug>/", view=missing_issues_list_view, name="category"),

    path("<str:category>/<str:slug>/skip_issue/<int:comicvine_id>/", view=skip_issue_view, name="category_skip_issue"),
    path("<str:category>/<str:slug>/skip_volume/<int:comicvine_id>/", view=skip_volume_view,
         name="category_skip_volume"),
    path("<str:category>/<str:slug>/skip_publisher/<int:comicvine_id>/", view=skip_publisher_view,
         name="category_skip_publisher"),

    path("<str:category>/<str:slug>/ignore_issue/<int:comicvine_id>/", view=ignore_issue_view,
         name="category_ignore_issue"),
    path("<str:category>/<str:slug>/ignore_volume/<int:comicvine_id>/", view=ignore_volume_view,
         name="category_ignore_volume"),
    path("<str:category>/<str:slug>/ignore_publisher/<int:comicvine_id>/", view=ignore_publisher_view,
         name="category_ignore_publisher"),

]
