from django.contrib import admin, messages

from metingen.models import MetRefPuntenHerz, MetingHerzien


class ControleActionsMixin:
    @admin.action(description="Maak grafiek")
    def make_graph(self, request, queryset):
        queryset = self._get_selection(queryset, request)
        self.measurement_points = queryset

    @admin.action(description="Sla metingen op")
    def save_measurements(self, request, queryset):
        queryset = self._get_selection(queryset, request)

        metingtype_is_consistent = all(m.metingtype == queryset[0].metingtype for m in queryset)
        if not metingtype_is_consistent:
            self.message_user(request, "De metingen hebben verschillende metingtypes", level=messages.ERROR)
            return

        metingtype = queryset[0].metingtype
        if metingtype.omschrijving == "Deformatiemeting":
            self.save_deformatie_metingen(queryset)
        elif metingtype.omschrijving == "NAP-meting":
            self.save_NAP_metingen(queryset)
        else:
            self.message_user(request, "Het metingtype wordt niet herkend", level=messages.ERROR)
        queryset.delete()

    def save_deformatie_metingen(self, queryset):
        queryset = list(queryset)
        metingen = [m for m in queryset if m.hoogtepunt.type.nummer == 7]
        ref_points = set([m.hoogtepunt for m in queryset if m not in metingen])  # Make unique set

        saved_metingen = self.save_metingen(metingen)
        meting_ref_points = []
        for meting in saved_metingen:
            meting_ref_points += [MetRefPuntenHerz(meting=meting, hoogtepunt=point) for point in ref_points]
        MetRefPuntenHerz.objects.bulk_create(meting_ref_points)

    def save_NAP_metingen(self, queryset):
        self.save_metingen(queryset)

    def save_metingen(self, queryset):
        saved_metingen = []
        for meting in queryset:
            data = {k: v for k, v in meting.__dict__.items() if not k.startswith("_")}
            if data.get("id"):
                data.pop("id")
            saved_metingen.append(MetingHerzien(**data))
        return MetingHerzien.objects.bulk_create(saved_metingen)

    @staticmethod
    def _get_selection(queryset, request):
        selected = request.POST.getlist("_selected_action")
        if selected:
            queryset = queryset.filter(pk__in=selected)
        return queryset