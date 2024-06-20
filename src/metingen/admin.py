from django.contrib import admin
from django.db.models import Count
from import_export.admin import ImportExportMixin, ImportMixin
from import_export.tmp_storages import CacheStorage
from leaflet.admin import LeafletGeoAdminMixin

from admin_chart.admin import AdminChartMixin

from .actions import ControleActionsMixin
from .form import CustomConfirmImportForm, CustomImportForm, HoogtepuntForm
from .formatters import CORFormatClass, TCOFormatClass
from .models import *
from .resource import MetingControleResource, MetingVerrijkingResource


class BouwblokListFilter(admin.SimpleListFilter):
    title = "Aantal Bouwblokken"
    parameter_name = "bouwblokken"

    def lookups(self, request, model_admin):
        return [
            ("0", "Geen bouwblokken"),
            ("1", "Een enkel bouwblok"),
            ("more", "Meerdere bouwblokken"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.filter(kringpunt__isnull=True)
        if self.value() == "1":
            return queryset.annotate(kringpunt_count=Count("kringpunt")).filter(
                kringpunt_count=1
            )
        if self.value() == "more":
            return queryset.annotate(kringpunt_count=Count("kringpunt")).filter(
                kringpunt_count__gt=1
            )


@admin.register(Hoogtepunt)
class HoogtepuntAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    admin_priority = 1
    tmp_storage_class = CacheStorage
    form = HoogtepuntForm
    modifiable = False  # Make the leaflet map read-only
    readonly_fields = ["nummer"]
    search_fields = ("omschrijving", "nummer")
    ordering = ("nummer",)
    list_filter = ("vervaldatum", BouwblokListFilter, "status", "type")
    list_display = (
        "nummer",
        "type",
        "get_bouwblokken",
        "merk",
        "status",
        "get_hoogte",
        "omschrijving",
        "vervaldatum",
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

    @admin.display(description="Kringpunt in bouwblokken")
    def get_bouwblokken(self, obj):
        return ", ".join([k.bouwblok.nummer for k in obj.kringpunt_set.all()])

    @admin.display(description="Laatst gemeten hoogte")
    def get_hoogte(self, obj):
        return obj.metingherzien_set.latest().hoogte


@admin.register(MetingVerrijking)
class MetingVerrijkingAdmin(ImportExportMixin, admin.ModelAdmin):
    admin_priority = 2
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
    raw_id_fields = ("hoogtepunt",)
    ordering = ("hoogtepunt",)
    resource_classes = [MetingVerrijkingResource]
    skip_export_form= True

    def get_import_formats(self):
        return [TCOFormatClass]

    def get_export_formats(self):
        return [TCOFormatClass]

    def has_add_permission(self, request):
        # Remove add button
        return False

    def get_export_filename(self, request, queryset, file_format):
        file_name = MetingVerrijking.objects.first().file_name
        MetingVerrijking.objects.all().delete()
        return file_name

    def get_import_data_kwargs(self, request, *args, **kwargs):
        """
        Prepare kwargs for import_data.
        """
        form = kwargs.get("form")
        if form:
            kwargs.pop("form")
            return form.cleaned_data
        return {}


@admin.register(MetingControle)
class MetingControleAdmin(
    AdminChartMixin, ImportMixin, ControleActionsMixin, admin.ModelAdmin
):
    admin_priority = 3
    list_display = (
        "hoogtepunt",
        "inwindatum",
        "hoogte",
        "sigmaz",
        "bron",
        "wijze_inwinning",
        "metingtype",
    )
    raw_id_fields = ("hoogtepunt",)
    actions = ["make_graph", "save_measurements"]
    tmp_storage_class = CacheStorage
    resource_classes = [MetingControleResource]
    import_form_class = CustomImportForm
    confirm_form_class = CustomConfirmImportForm

    def has_add_permission(self, request):
        # Remove add button
        return False

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


@admin.register(MetingHerzien)
class MetingHerzienAdmin(admin.ModelAdmin):
    admin_priority = 4
    list_display = (
        "id",
        "hoogtepunt",
        "inwindatum",
        "wijze_inwinning",
        "sigmaz",
        "bron",
        "hoogte",
        "metingtype",
    )
    raw_id_fields = ("hoogtepunt",)
    search_fields = ("hoogtepunt__nummer",)
    ordering = ("-inwindatum",)
    list_filter = ("inwindatum", "wijze_inwinning", "metingtype", "bron")


@admin.register(MetRefPuntenHerz)
class MetingReferentiepuntAdmin(admin.ModelAdmin):
    admin_priority = 5
    list_display = ("hoogtepunt", "meting", "get_bouwblok")
    raw_id_fields = ("hoogtepunt", "meting")
    search_fields = ("hoogtepunt__nummer", "meting__id")
    list_filter = ("meting__inwindatum",)
    ordering = ("-meting__inwindatum",)

    @admin.display(description="Meting op Bouwblok")
    def get_bouwblok(self, obj):
        kringpunten = obj.meting.hoogtepunt.kringpunt_set.all()
        if kringpunten:
            return ", ".join([k.bouwblok.nummer for k in kringpunten])
        return None


def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    app_dict = self._build_app_dict(request, app_label)

    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

    for app in app_list:
        app["models"].sort(key=lambda x: getattr(x, "admin_priority", 20))

    return app_list


admin.AdminSite.get_app_list = get_app_list
