import requests
from django.conf import settings
from django.views.generic import TemplateView
from requests.exceptions import JSONDecodeError


class ControlTemplateView(TemplateView):
    template_name = "funicular_down/control.html"


class GetStatusTemplateView(TemplateView):
    template_name = "funicular_down/control.html"

    def get_context_data(self, **kwargs):
        headers = {"Authorization": f"Token {settings.FUNICULAR_TOKEN}"}
        context = super().get_context_data(**kwargs)
        r = requests.get(
            f"{settings.FUNICULAR_HOST}/pics/status/",
            headers=headers,
        )
        try:
            uploaded = r.json()
        except JSONDecodeError:
            context["status"] = f"JSON encode error - {r.text}"
        for id, url in uploaded.items():
            r = requests.get(
                f"{settings.FUNICULAR_HOST}{url}",
            )
        context["status"] = uploaded
        return context
