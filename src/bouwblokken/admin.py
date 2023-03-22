from django.contrib import admin
from .models import *
from .actions import BouwblokActionsMixin


@admin.register(Bouwblok)
class BouwblokAdmin(admin.ModelAdmin, BouwblokActionsMixin):
    actions = ["get_report"]
    list_display = (
        "aansluitpunt",
        "controlepunt",
        "opmerking"
    )


@admin.register(Referentiepunt)
class ReferentiepuntAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "bouwblok",
    )


@admin.register(Controlepunt)
class ControlepuntAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "bouwblok",
    )


@admin.register(Kringpunt)
class KringpuntAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "bouwblok",
        "volgorde",
    )