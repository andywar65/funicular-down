import requests
from django.conf import settings
from django.views.generic import TemplateView


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
        context["status"] = r.json()
        return context
