from django.urls import path

from .views import team_detail_view, teams_list_view

app_name = "teams"
urlpatterns = [
    path("", view=teams_list_view, name="list"),
    path("<str:slug>/", view=team_detail_view, name="detail"),
]
