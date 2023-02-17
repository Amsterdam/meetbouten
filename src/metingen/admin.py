# from cffi.setuptools_ext import execfile
from datetime import datetime
from django.contrib import admin
from import_export.admin import ImportMixin
from .resource import MetingControleResource
from .cor_loader import CORFormatClass


# from django.utils.html import format_html
from admincharts.admin import AdminChartMixin

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

    search_fields = ('nummer',)


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
class MetingControleAdmin(AdminChartMixin, ImportMixin, admin.ModelAdmin):
    resource_classes = [MetingControleResource]
    list_display = (
        "hoogtepunt",
        "inwindatum",
        "x",
        "y",
        "hoogte",
    )
    list_chart_type = "line"
    list_chart_options = {
        "aspectRatio": 6,
        "spanGaps": True,
        "autoSkip": True,
        "line": {"tension": 0.1},
        "scales": {
            "x": {
                "ticks": {
                    # 'callback': 'function(value, index) { return value; }',
                    # "color": "green"
                }
            }
        },
    }
    list_chart_config = None  # Override the combined settings
    actions = [make_graph]
    measurement_points = []

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        self.formats = list(set(self.formats + [CORFormatClass]))
        return [CORFormatClass]
        #return [f for f in self.formats if f().can_import()]


    def get_labels(self, querysets):
        return [str(qs[0].hoogtepunt) for qs in querysets]

    def get_list_chart_queryset(self, changelist):
        if self.measurement_points:
            querysets = []
            for mp in self.measurement_points:
                metingen = MetingHerzien.objects.filter(hoogtepunt=mp.hoogtepunt).order_by("inwindatum")
                # metingen.append(mp)  # Add the measurement point itself
                querysets.append(metingen)
            return querysets
        return []

    def get_list_chart_data(self, querysets):
        def get_datestr(datum):
            return datum.strftime("%Y-%m-%d")

        def get_timestamp(d):
            return datetime(d.year, d.month, d.day).timestamp()

        # Get labels
        date_labels = []
        for qs in querysets:
            for meting in qs:
                date = meting.inwindatum
                if date not in date_labels:
                    date_labels.append(date)
        date_labels.sort()
        timestamp_labels = [get_timestamp(date) for date in date_labels]

        datasets = []
        for qs in querysets:
            init_val = None
            hoogtes_dict = {ts: None for ts in timestamp_labels}
            for meting in qs:
                hoogtes_dict[get_timestamp(meting.inwindatum)] = meting.hoogte
                if not init_val:
                    init_val = meting.hoogte

            if init_val:
                if len(querysets) == 1:
                    hoogtes = [hoogtes_dict[ts] if hoogtes_dict[ts] else None for ts in timestamp_labels]
                else:
                    hoogtes = [hoogtes_dict[ts] - init_val if hoogtes_dict[ts] else None for ts in timestamp_labels]

                # data = [{'x': ts, 'y': hoogte} for ts, hoogte in zip(timestamp_labels, hoogtes)]
                label = str(qs[0].hoogtepunt)
                if label not in [ds["label"] for ds in datasets]:
                    datasets.append(
                        {
                            "label": label,
                            "data": hoogtes,
                            "backgroundColor": "green",
                            "color": "green",
                            "borderColor": "green",
                            "showLine": True,
                        }
                    )

        return {
            "labels": [get_datestr(date) for date in date_labels],
            "datasets": datasets,
        }


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
