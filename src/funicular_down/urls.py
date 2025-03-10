from django.urls import path

from .views import BaseTemplateView, GetStatusTemplateView

app_name = "funicular_down"
urlpatterns = [
    path("", BaseTemplateView.as_view(), name="home"),
    path("check/", GetStatusTemplateView.as_view(), name="check"),
]
