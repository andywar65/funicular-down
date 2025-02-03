from io import BytesIO

import requests
from django.conf import settings
from django.core.files import File
from django.views.generic import TemplateView
from requests.exceptions import JSONDecodeError

from .models import Entry


class ControlTemplateView(TemplateView):
    template_name = "funicular_down/control.html"


class GetStatusTemplateView(TemplateView):
    template_name = "funicular_down/control.html"

    def get_context_data(self, **kwargs):
        headers = {"Authorization": f"Token {settings.FUNICULAR_TOKEN}"}
        context = super().get_context_data(**kwargs)
        context["status"] = ""
        r = requests.get(
            f"{settings.FUNICULAR_HOST}/pics/status/",
            headers=headers,
        )
        try:
            uploaded = r.json()
        except JSONDecodeError:
            context["status"] = f"JSON encode error - {r.text}"
        for id, url in uploaded.items():
            name = url.split("/")[-1]
            r = requests.get(
                f"{settings.FUNICULAR_HOST}{url}",
            )
            e = Entry()
            e.id_up = int(id)
            e.image.save(name, File(BytesIO(r.content)))
            e.save()
            context["status"] += f"Created {id} - {name}\n"
        return context
