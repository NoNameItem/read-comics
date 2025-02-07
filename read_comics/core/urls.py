from django.urls import path
from django.views.generic import TemplateView

from .views import home_view, metrics_view, new_issues_view

app_name = "core"
urlpatterns = [
    path("", view=home_view, name="home"),
    path("metrics/", view=metrics_view, name="metrics"),
    path("robots.txt", TemplateView.as_view(template_name="core/robots.txt", content_type="text/plain")),
    path("new_issues/<int:year>/<int:month>/<int:day>/", view=new_issues_view, name="new_issues"),
]
