from django.urls import path

from .views import ControlTemplateView, GetStatusTemplateView

app_name = "funicular_down"
urlpatterns = [
    path("control/", ControlTemplateView.as_view(), name="control"),
    path("status/", GetStatusTemplateView.as_view(), name="status"),
]
