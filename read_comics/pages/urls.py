from django.urls import path

from .views import home_view

app_name = "pages"
urlpatterns = [
    path("", view=home_view, name="home"),
]
