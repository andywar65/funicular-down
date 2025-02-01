import requests
from django.conf import settings
from django.views.generic import TemplateView
from requests.exceptions import JSONDecodeError


class ControlTemplateView(TemplateView):
    template_name = "funicular_down/control.html"


class GetStatusTemplateView(TemplateView):
    template_name = "funicular_down/control.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = requests.get(
            f"{settings.FUNICULAR_HOST}/pics/status/",
            auth=(settings.FUNICULAR_USER, settings.FUNICULAR_PWD),
        )
        try:
            context["status"] = r.json()
        except JSONDecodeError:
            context["status"] = "JSON decode error"
        return context
