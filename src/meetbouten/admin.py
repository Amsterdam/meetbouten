from django.contrib import admin
# from django.utils.html import format_html
from admincharts.admin import AdminChartMixin
from django.db.models import Count

from .models import Grondslagpunt, Type


@admin.register(Type)
class MeetboutChartAdmin(AdminChartMixin, admin.ModelAdmin):
    list_display = ('omschrijving', 'soort')

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

    list_chart_type = "bar"
    list_chart_options = {"aspectRatio": 6}
    list_chart_config = None  # Override the combined settings

    def get_list_chart_data(self, changelist):
        return {
            "labels": ["test1", "test2", "test3"],
            "datasets": [
                {"label": "New accounts", "data": [7,3,8], "backgroundColor": "green"},
            ],
        }
