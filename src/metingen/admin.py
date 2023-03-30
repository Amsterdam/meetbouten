from django.contrib import admin
from import_export.admin import ImportExportMixin, ImportMixin
from import_export.tmp_storages import CacheStorage
from leaflet.admin import LeafletGeoAdminMixin

from admin_chart.admin import AdminChartMixin

from .actions import ControleActionsMixin
from .form import CustomConfirmImportForm, CustomImportForm, HoogtepuntForm
from .formatters import CORFormatClass, TCOFormatClass
from .models import *
from .resource import MetingControleResource, MetingVerrijkingResource


@admin.register(Hoogtepunt)
class HoogtepuntAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    tmp_storage_class = CacheStorage
    form = HoogtepuntForm
    modifiable = False  # Make the leaflet map read-only
    readonly_fields = ["nummer"]
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
        "picture_tag",
    )
    fieldsets = (
        (
            None,
            {
                "fields": ("nummer",),
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "type",
                    "merk",
                    "status",
                    "agi_nummer",
                    "vervaldatum",
                    "omschrijving",
                    "picture",
                ),
            },
        ),
        (
            "Positie",
            {
                "fields": ("xmuur", "ymuur", "windr", "sigmax", "sigmay", "orde"),
            },
        ),
        (
            "Locatie",
            {
                "fields": ("x", "y", "geom"),
            },
        ),
    )


@admin.register(Grondslagpunt)
class GrondslagpuntAdmin(admin.ModelAdmin):
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


@admin.register(MetingControle)
class MetingControleAdmin(
    AdminChartMixin, ImportMixin, ControleActionsMixin, admin.ModelAdmin
):
    list_display = (
        "hoogtepunt",
        "inwindatum",
        "hoogte",
        "sigmaz",
        "bron",
        "wijze_inwinning",
        "metingtype",
    )
    actions = ["make_graph", "save_measurements"]
    tmp_storage_class = CacheStorage
    resource_class = MetingControleResource
    import_form_class = CustomImportForm
    confirm_form_class = CustomConfirmImportForm

    def get_import_formats(self):
        return [CORFormatClass]

    def get_confirm_form_initial(self, request, import_form):
        # Pass the import form data to the confirm form
        initial = super().get_confirm_form_initial(request, import_form)
        if import_form:
            fields = ["wijze_inwinning", "bron", "metingtype", "inwindatum"]
            for f in fields:
                initial[f] = import_form.cleaned_data[f]
        return initial

    def get_import_data_kwargs(self, request, *args, **kwargs):
        """
        Prepare kwargs for import_data.
        """
        form = kwargs.get("form")
        if form:
            kwargs.pop("form")
            return form.cleaned_data
        return {}


@admin.register(MetRefPuntenHerz)
class MetingReferentiepuntAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "meting",
    )


@admin.register(MetingVerrijking)
class MetingVerrijkingAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "x",
        "y",
        "hoogte",
        "inwindatum",
        "c1",
        "c2",
        "c3",
    )
    ordering = ("hoogtepunt",)
    resource_class = MetingVerrijkingResource

    def get_import_formats(self):
        return [TCOFormatClass]

    def get_export_formats(self):
        return [TCOFormatClass]
