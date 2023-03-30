from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook

from bouwblokken.models import Kringpunt
from metingen.models import Hoogtepunt, MetingHerzien


class BouwblokActionsMixin:
    @admin.action(description="Maak rapportage")
    def get_report(self, request, queryset):
        filename = f"report-{datetime.today().strftime('%Y-%m-%d')}.xlsx"
        field_names = [
            "Bouwblok nummer",
            "Hoogtepunt nummer",
            "Inwindatum",
            "Hoogte",
            "Verschil vorig",
            "Verschil nulmeting",
        ]
        data = self.collect_data(queryset)

        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        [ws.append(row) for row in data]

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}.xlsx"
        wb.save(response)
        return response

    def collect_data(self, queryset):
        data = []
        for bouwblok in queryset:
            hoogtepunten = Hoogtepunt.objects.filter(
                id__in=Kringpunt.objects.filter(bouwblok=bouwblok).values("hoogtepunt")
            ).order_by("nummer")
            for hoogtepunt in hoogtepunten:
                metingen = MetingHerzien.objects.filter(
                    hoogtepunt=hoogtepunt.id
                ).order_by("inwindatum")
                start_meting = metingen.first()
                if not start_meting:
                    continue
                start_hoogte = start_meting.hoogte
                laatste_hoogte = start_hoogte
                for meting in metingen:
                    data.append(
                        [
                            bouwblok.nummer,
                            hoogtepunt.nummer,
                            meting.inwindatum,
                            round(meting.hoogte, 4),
                            round(meting.hoogte - laatste_hoogte, 4),
                            round(meting.hoogte - start_hoogte, 4),
                        ]
                    )
                    laatste_hoogte = meting.hoogte
        return data
