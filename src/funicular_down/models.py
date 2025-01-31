from django.db import models
from django.utils.translation import gettext_lazy as _


class Entry(models.Model):
    id_up = models.PositiveBigIntegerField(editable=False)
    image = models.ImageField(_("Image"), upload_to="funicular/")

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")

    def __str__(self):
        return f"Entry - {self.id}"
