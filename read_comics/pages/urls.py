from django.urls import path
from django.views.generic import TemplateView

from .views import home_view

app_name = "pages"
urlpatterns = [
    path("", view=home_view, name="home"),
    path("robots.txt", TemplateView.as_view(template_name="pages/robots.txt", content_type="text/plain")),
]
