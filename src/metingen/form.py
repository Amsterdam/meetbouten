from django import forms
from import_export.forms import ImportForm, ConfirmImportForm

from referentie_tabellen.models import Metingtype, Bron, WijzenInwinning


class FormMixin(forms.Form):
    inwindatum = forms.DateTimeField(
        widget=forms.DateInput(attrs={"type": "date", "placeholder": "yyyy-mm-dd (DOB)", "class": "form-control"}),
        label="Inwindatum",
        required=True,
    )
    wijze_inwinning = forms.ModelChoiceField(queryset=WijzenInwinning.objects.all(), required=True)
    bron = forms.ModelChoiceField(queryset=Bron.objects.all(), required=True)
    metingtype = forms.ModelChoiceField(queryset=Metingtype.objects.all(), required=True)


class CustomImportForm(FormMixin, ImportForm):
    pass


class CustomConfirmImportForm(FormMixin, ConfirmImportForm):
    pass
