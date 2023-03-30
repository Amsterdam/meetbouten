import pytest

from admin_chart.admin import AdminChartMixin
from metingen.factories import (
    HoogtepuntFactory,
    MetingControleFactory,
    MetingHerzFactory,
)


@pytest.mark.django_db
class TestAdminChartMixin:
    def test_get_list_chart_queryset_empty(self):
        admin = AdminChartMixin()
        hp = HoogtepuntFactory()
        mp = MetingControleFactory(hoogtepunt=hp)
        admin.measurement_points = [mp]

        querysets = admin.get_list_chart_queryset(None)

        assert len(querysets) == 1

    def test_get_list_chart_queryset(self):
        admin = AdminChartMixin()
        hp = HoogtepuntFactory()
        mp = MetingControleFactory(hoogtepunt=hp)
        historic_measurements = MetingHerzFactory.create_batch(5, hoogtepunt=hp)
        admin.measurement_points = [mp] + historic_measurements

        querysets = admin.get_list_chart_queryset(None)

        assert len(querysets) == 6

    def test_get_list_chart_data(self):
        hp = HoogtepuntFactory()
        queryset = MetingHerzFactory.create_batch(5, hoogtepunt=hp)

        datasets = AdminChartMixin().get_list_chart_data([queryset])

        assert len(datasets["datasets"]) == 1
        assert datasets["datasets"][0]["label"] == str(hp)
        assert datasets["datasets"][0]["data"] == [
            {"x": meting.inwindatum, "y": meting.hoogte} for meting in queryset
        ]

    def test_get_list_chart_data_multiple(self):
        hp_1 = HoogtepuntFactory()
        queryset_1 = MetingHerzFactory.create_batch(5, hoogtepunt=hp_1)
        hp_2 = HoogtepuntFactory()
        queryset_2 = MetingHerzFactory.create_batch(5, hoogtepunt=hp_2)

        datasets = AdminChartMixin().get_list_chart_data([queryset_1, queryset_2])

        assert len(datasets["datasets"]) == 2
        assert datasets["datasets"][0]["label"] == str(hp_1)
        assert datasets["datasets"][1]["label"] == str(hp_2)
        init_val_1 = queryset_1[0].hoogte
        assert datasets["datasets"][0]["data"] == [
            {"x": meting.inwindatum, "y": meting.hoogte - init_val_1}
            for meting in queryset_1
        ]
