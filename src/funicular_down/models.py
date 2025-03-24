from io import BytesIO

import requests
from django.core.files import File
from django.db import IntegrityError, models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from requests.exceptions import JSONDecodeError


class Server(models.Model):
    url = models.URLField(_("Address"))
    token = models.CharField(_("Token Key"), max_length=40)
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Server")
        verbose_name_plural = _("Servers")

    def __str__(self):
        return self.url


class Entry(models.Model):
    server = models.ForeignKey(
        Server, verbose_name=_("Server"), editable=False, on_delete=models.CASCADE
    )
    id_up = models.PositiveBigIntegerField(editable=False, unique=True)
    image = models.ImageField(_("Image"), upload_to="funicular/")

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")

    def __str__(self):
        return f"Entry - {self.id}"


def get_status_from_server(server):
    headers = {"Authorization": f"Token {server.token}"}
    status = ""
    r = requests.get(
        f"{server.url}/pics/status/",
        headers=headers,
    )
    try:
        uploaded = r.json()
    except JSONDecodeError:
        status = f"<p>JSON encode error - {r.text}</p>"
    for id, data in uploaded.items():
        if data == "Invalid token.":
            return "Invalid token"
        if data["status"] == "UP":
            name = data["url"].split("/")[-1]
            r = requests.get(
                f"{server.url}{data["url"]}",
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
                    f"{server.url}/pics/entry/{id}/download/",
                    headers=headers,
                )
                try:
                    message = r.json()
                    status += f"<p>{message["text"]}</p>"
                except JSONDecodeError:
                    status += f"<p>JSON encode error - {r.text}</p>"
        elif data["status"] == "KI":
            r = requests.get(
                f"{server.url}/pics/entry/{id}/download/",
                headers=headers,
            )
            try:
                message = r.json()
                status += f"<p>{message["text"]}</p>"
            except JSONDecodeError:
                status += f"<p>JSON encode error - {r.text}</p>"
        elif data["status"] == "RQ":
            entry = get_object_or_404(Entry, id_up=id)
            name = entry.image.url.split("/")[-1]
            ext = name.split(".")[1]
            with open(entry.image.path, "rb") as image_file:
                files = {"image": (name, image_file, f"image/{ext}")}
                r = requests.put(
                    f"{server.url}/pics/entry/{id}/upload/",
                    files=files,
                    headers=headers,
                )
            try:
                message = r.json()
                if "text" in message:
                    status += f"<p>{message["text"]}</p>"
                else:
                    status += f"<p>{message}</p>"
            except JSONDecodeError:
                status += f"<p>JSON encode error - {r.text}</p>"

    return status
