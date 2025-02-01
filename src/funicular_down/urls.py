from django.urls import path

from .views import ControlTemplateView

app_name = "funicular_down"
urlpatterns = [
    path("control/", ControlTemplateView.as_view(), name="control"),
]
