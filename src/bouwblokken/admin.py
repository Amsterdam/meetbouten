from django.contrib import admin
from .models import *


@admin.register(Bouwblok)
class BouwblokAdmin(admin.ModelAdmin):
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