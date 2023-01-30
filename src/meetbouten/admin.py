# from cffi.setuptools_ext import execfile
from django.contrib import admin

# from django.utils.html import format_html
from admincharts.admin import AdminChartMixin
from django.db.models import Count

from .models import Grondslagpunt, Type, Bron, Hoogtepunt, MetingHerzien, Merk, Status


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("omschrijving", "soort")


@admin.register(Merk)
class MerkAdmin(admin.ModelAdmin):
    list_display = ("omschrijving", "omschrijving_verkort")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("omschrijving",)


@admin.register(Bron)
class BronAdmin(admin.ModelAdmin):
    list_display = ("omschrijving", "doel")


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
class MeetboutChartAdmin(AdminChartMixin, admin.ModelAdmin):
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

    list_chart_type = "line"
    list_chart_options = {"aspectRatio": 6}
    list_chart_config = None  # Override the combined settings

    def get_list_chart_data(self, changelist):
        return {
            "labels": ["test1", "test2", "test3", "test4", "test5"],
            "datasets": [
                {
                    "label": "New accounts",
                    "data": [7, 6, 5, 3, 2],
                    "backgroundColor": "green",
                    "color": "green",
                    "borderColor": "green",
                },
            ],
        }


@admin.register(MetingHerzien)
class MetingHerzienChartAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "inwindatum",
        "wijze_inwinning",
        "sigmaz",
        "bron",
        "hoogte",
        "metingtype",
    )

