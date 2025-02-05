from io import BytesIO

import requests
from django.conf import settings
from django.core.files import File
from django.db import IntegrityError
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
            context["status"] = f"<p>JSON encode error - {r.text}</p>"
        for id, url in uploaded.items():
            name = url.split("/")[-1]
            r = requests.get(
                f"{settings.FUNICULAR_HOST}{url}",
            )
            e = Entry()
            e.id_up = int(id)
            e.image.save(name, File(BytesIO(r.content)), save=False)
            try:
                e.save()
                context["status"] += f"<p>Downloaded {id} - {name}</p>"
                downloaded = True
            except IntegrityError:
                context["status"] += f"<p>Already downloaded {id}</p>"
                downloaded = False
            if downloaded:
                r = requests.get(
                    f"{settings.FUNICULAR_HOST}/pics/entry/{id}/downloaded/",
                    headers=headers,
                )
                try:
                    message = r.json()  # noqa
                    context["status"] += f"<p>{message["text"]}</p>"
                except JSONDecodeError:
                    context["status"] += f"<p>JSON encode error - {r.text}</p>"
        return context
