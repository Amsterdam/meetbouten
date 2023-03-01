# from cffi.setuptools_ext import execfile
from datetime import datetime
from django.contrib import admin

# from django.utils.html import format_html
from admin_chart.admin import AdminChartMixin

from .models import *


@admin.register(Hoogtepunt)
class HoogtepuntChartAdmin(admin.ModelAdmin):
    list_display = (
        "nummer",
        "type",
        "agi_nummer",
        "vervaldatum",
        "omschrijving",
        "merk",
        "xmuur",
        "ymuur",
        "windr",
        "sigmax",
        "sigmay",
        "status",
        "orde",
    )


@admin.register(Grondslagpunt)
class GrondslagpuntChartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "inwindatum",
        "vervaldatum",
        "sigmax",
        "sigmay",
        "sigmaz",
        "omschrijving",
        # "picture_tag",
    )
    list_filter = ("inwindatum", "vervaldatum")
    search_fields = ("nummer", "type_nummer", "omschrijving")
    # readonly_fields = ('picture_tag',)


@admin.register(Meting)
class MetingAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "inwindatum",
        "wijze_inwinning",
        "sigmaz",
        "bron",
        "hoogte",
        "metingtype",
    )


@admin.register(MetingHerzien)
class MetingHerzienAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "inwindatum",
        "wijze_inwinning",
        "sigmaz",
        "bron",
        "hoogte",
        "metingtype",
    )


@admin.action(description="Maak grafiek")
def make_graph(modeladmin, request, queryset):
    selected = request.POST.getlist("_selected_action")
    if selected:
        queryset = queryset.filter(pk__in=selected)
    modeladmin.measurement_points = queryset


@admin.register(MetingControle)
class MetingControleAdmin(AdminChartMixin, admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "inwindatum",
        "x",
        "y",
        "hoogte",
    )
    actions = [make_graph]


@admin.register(MetingReferentiepunt)
class MetingReferentiepuntAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "meting",
    )


@admin.register(MetRefPuntenHerz)
class MetRefPuntenHerzAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "meting",
    )
