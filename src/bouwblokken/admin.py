from django.contrib import admin

from .actions import BouwblokActionsMixin
from .models import *


@admin.register(Bouwblok)
class BouwblokAdmin(admin.ModelAdmin, BouwblokActionsMixin):
    actions = ["get_report"]
    list_display = ("nummer", "aansluitpunt", "controlepunt", "opmerking")


@admin.register(Referentiepunt)
class ReferentiepuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
    )


@admin.register(Controlepunt)
class ControlepuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
    )


@admin.register(Kringpunt)
class KringpuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
        "volgorde",
    )
