from django.urls import path

from .views import GetStatusTemplateView

app_name = "funicular_down"
urlpatterns = [
    path("check/", GetStatusTemplateView.as_view(), name="check"),
]
