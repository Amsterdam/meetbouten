from django import forms
from django.contrib.gis.geos import Point
from import_export.forms import ImportForm, ConfirmImportForm

from metingen.models import Hoogtepunt
from referentie_tabellen.models import Metingtype, Bron, WijzenInwinning


class HoogtepuntForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control"}), label="X coördinaat")
    y = forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control"}), label="Y coördinaat")

    class Meta:
        model = Hoogtepunt
        exclude = ['']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        geom = self.initial.get("geom", None)
        if isinstance(geom, Point):
            self.initial["x"], self.initial["y"] = geom.tuple

    def clean(self):
        cleaned_data = super().clean()
        x, y = cleaned_data.pop('x', None), cleaned_data.pop('y', None)
        if x and y:
            cleaned_data["geom"] = f"POINT({x} {y})"
        else:
            raise forms.ValidationError({"geom": "X en Y moeten ingevuld zijn"})
        return cleaned_data

    def clean_x(self):
        x = self.cleaned_data["x"]
        if x > 0:
            return x
        raise forms.ValidationError("X moet groter dan 0 zijn")

    def clean_y(self):
        y = self.cleaned_data["y"]
        if y > 0:
            return y
        raise forms.ValidationError("Y moet groter dan 0 zijn")


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
