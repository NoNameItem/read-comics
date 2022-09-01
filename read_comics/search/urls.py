from django.urls import path

from .views import ajax_search_view, search_view

app_name = "search"
urlpatterns = [path("", view=search_view, name="search"), path("ajax/", view=ajax_search_view, name="ajax")]
