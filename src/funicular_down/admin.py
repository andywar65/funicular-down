from django.contrib import admin

from .models import Entry, Server


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "server",
        "id_up",
        "image",
    )


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("url",)
