from django.contrib import admin

from .actions import BouwblokActionsMixin
from .models import *


@admin.register(Bouwblok)
class BouwblokAdmin(admin.ModelAdmin, BouwblokActionsMixin):
    actions = ["get_report_bouwblok", "get_report_history"]
    list_display = ("nummer", "aansluitpunt", "controlepunt", "opmerking")
    raw_id_fields = ("aansluitpunt", "controlepunt")


@admin.register(Referentiepunt)
class ReferentiepuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
    )
    raw_id_fields = ("hoogtepunt", "bouwblok")


@admin.register(Controlepunt)
class ControlepuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
    )
    raw_id_fields = ("hoogtepunt", "bouwblok")


@admin.register(Kringpunt)
class KringpuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
        "volgorde",
    )
    raw_id_fields = ("hoogtepunt", "bouwblok")
