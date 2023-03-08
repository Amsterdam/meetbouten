# from cffi.setuptools_ext import execfile

from django.contrib import admin

# from django.utils.html import format_html
from import_export.tmp_storages import CacheStorage

from admin_chart.admin import AdminChartMixin
from import_export.admin import ImportMixin

from .resource import MetingControleResource
from .cor_loader import CORFormatClass
from .form import CustomImportForm, CustomConfirmImportForm
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
    list_display = (
        "hoogtepunt",
        "inwindatum",
        "hoogte",
        "sigmaz",
        "bron",
        "wijze_inwinning",
        "metingtype",
    )
    actions = [make_graph]
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
        form = kwargs.get('form')
        if form:
            kwargs.pop('form')
            return form.cleaned_data
        return {}


@admin.register(MetRefPuntenHerz)
class MetingReferentiepuntAdmin(admin.ModelAdmin):
    list_display = (
        "hoogtepunt",
        "meting",
    )