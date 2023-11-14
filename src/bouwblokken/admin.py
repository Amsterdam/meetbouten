from django.contrib import admin

from .actions import BouwblokActionsMixin
from .models import *


@admin.register(Bouwblok)
class BouwblokAdmin(admin.ModelAdmin, BouwblokActionsMixin):
    actions = ["get_report_bouwblok", "get_report_history"]
    list_display = ("nummer", "aansluitpunt", "controlepunt", "opmerking", "get_referentiepunten", "get_kringpunten")
    raw_id_fields = ("aansluitpunt", "controlepunt")
    search_fields = ("nummer", "aansluitpunt__nummer", "controlepunt__nummer", "opmerking")
    ordering = ("nummer",)

    @admin.display(description='Referentiepunten')
    def get_referentiepunten(self, obj):
        return ", ".join([p.hoogtepunt.nummer for p in obj.referentiepunt_set.all()])

    @admin.display(description='Kringpunten')
    def get_kringpunten(self, obj):
        return ", ".join([p.hoogtepunt.nummer for p in obj.kringpunt_set.all()])

@admin.register(Referentiepunt)
class ReferentiepuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
    )
    raw_id_fields = ("hoogtepunt", "bouwblok")
    search_fields = ("hoogtepunt__nummer", "bouwblok__nummer")
    ordering = ("bouwblok__nummer", "hoogtepunt__nummer")

@admin.register(Controlepunt)
class ControlepuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
    )
    raw_id_fields = ("hoogtepunt", "bouwblok")
    search_fields = ("hoogtepunt__nummer", "bouwblok__nummer")
    ordering = ("bouwblok__nummer", "hoogtepunt__nummer")


@admin.register(Kringpunt)
class KringpuntAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hoogtepunt",
        "bouwblok",
        "volgorde",
    )
    raw_id_fields = ("hoogtepunt", "bouwblok")
    search_fields = ("hoogtepunt__nummer", "bouwblok__nummer")
    ordering = ("bouwblok__nummer", "hoogtepunt__nummer", "volgorde")
