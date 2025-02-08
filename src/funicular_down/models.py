from io import BytesIO

import requests
from django.conf import settings
from django.core.files import File
from django.db import IntegrityError, models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from requests.exceptions import JSONDecodeError


class Entry(models.Model):
    id_up = models.PositiveBigIntegerField(editable=False, unique=True)
    image = models.ImageField(_("Image"), upload_to="funicular/")

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")

    def __str__(self):
        return f"Entry - {self.id}"


def get_status_from_server():
    headers = {"Authorization": f"Token {settings.FUNICULAR_TOKEN}"}
    status = ""
    r = requests.get(
        f"{settings.FUNICULAR_HOST}/pics/status/",
        headers=headers,
    )
    try:
        uploaded = r.json()
    except JSONDecodeError:
        status = f"<p>JSON encode error - {r.text}</p>"
    for id, data in uploaded.items():
        if data["status"] == "UP":
            name = data["url"].split("/")[-1]
            r = requests.get(
                f"{settings.FUNICULAR_HOST}{data["url"]}",
            )
            e = Entry()
            e.id_up = int(id)
            e.image.save(name, File(BytesIO(r.content)), save=False)
            try:
                e.save()
                status += f"<p>Downloaded image {id} - {name}</p>"
                downloaded = True
            except IntegrityError:
                status += f"<p>Already downloaded image {id}</p>"
                downloaded = False
            if downloaded:
                r = requests.get(
                    f"{settings.FUNICULAR_HOST}/pics/entry/{id}/downloaded/",
                    headers=headers,
                )
                try:
                    message = r.json()
                    status += f"<p>{message["text"]}</p>"
                except JSONDecodeError:
                    status += f"<p>JSON encode error - {r.text}</p>"
        elif data["status"] == "KI":
            r = requests.get(
                f"{settings.FUNICULAR_HOST}/pics/entry/{id}/downloaded/",
                headers=headers,
            )
            try:
                message = r.json()
                status += f"<p>{message["text"]}</p>"
            except JSONDecodeError:
                status += f"<p>JSON encode error - {r.text}</p>"
        elif data["status"] == "RQ":
            entry = get_object_or_404(Entry, id_up=id)
            files = {"file": open(entry.image.path, "rb")}
            r = requests.put(
                f"{settings.FUNICULAR_HOST}/pics/entry/{id}/uploaded/",
                files=files,
                data={"status": "ST"},
                headers=headers,
            )

    return status
