from django.contrib import admin
from django.utils.html import format_html

from .models import Meetbout


@admin.register(Meetbout)
class MeetboutAdmin(admin.ModelAdmin):
    list_display = (
        "nummer",
        "type_nummer",
        "inwindatum",
        "vervaldatum",
        "sigmax",
        "sigmay",
        "sigmaz",
        "omschrijving",
        "picture_tag",
    )
    list_filter = ("inwindatum", "vervaldatum")
    search_fields = ("nummer", "type_nummer", "omschrijving")
    readonly_fields = ('picture_tag',)
