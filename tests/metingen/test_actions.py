from unittest.mock import Mock, MagicMock

import pytest
from django.contrib.admin import AdminSite
from django.core.checks import messages

from metingen.admin import MetingControleAdmin
from metingen.factories import MetingControleFactory, HoogtepuntFactory
from metingen.models import MetingHerzien, MetingControle, MetRefPuntenHerz
from referentie_tabellen.models import Metingtype, Type

@pytest.fixture
def model_admin():
    site = AdminSite()
    return MetingControleAdmin(MetingControle, site)


@pytest.fixture
def metingtype_deformatie():
    return Metingtype.objects.get(pk=1)


@pytest.fixture
def metingtype_nap():
    return Metingtype.objects.get(pk=2)


@pytest.mark.django_db
class TestActions:
    def test_make_graph(self, client, model_admin):
        hoogtepunt = HoogtepuntFactory.create()
        MetingControleFactory.create_batch(5, hoogtepunt=hoogtepunt)
        metingen = MetingControle.objects.all()
        metingen_selected = [f.pk for f in metingen[:2]]

        request = Mock()
        request.POST.getlist.return_value = metingen_selected

        model_admin.make_graph(request, metingen)

        measurement_points = MetingControle.objects.filter(pk__in=metingen_selected)
        assert [m for m in model_admin.measurement_points] == [m for m in measurement_points]

    def test_save_inconsistent_measurements(self, client, model_admin, metingtype_nap, metingtype_deformatie):
        hoogtepunt = HoogtepuntFactory.create()
        MetingControleFactory.create_batch(5, hoogtepunt=hoogtepunt, metingtype=metingtype_deformatie)
        MetingControleFactory.create_batch(5, hoogtepunt=hoogtepunt, metingtype=metingtype_nap)
        metingen = MetingControle.objects.all()

        request = Mock()
        request.POST.getlist.return_value = [f.pk for f in metingen]

        model_admin.save_measurements(request, metingen)

        assert MetingControle.objects.count() == len(metingen)
        assert MetingHerzien.objects.count() == 0
        request.POST.getlist.assert_called_once()
        request._messages.add.assert_called_with(messages.ERROR, 'De metingen hebben verschillende metingtypes', '')

    def test_save_deformatie_measurements(self, client, model_admin, metingtype_deformatie):
        bout_types = [7, 7, 7, 7, 6, 8, 9]
        for type_nr in bout_types:
            MetingControleFactory.create(
                hoogtepunt=HoogtepuntFactory.create(type=Type.objects.get(pk=type_nr)),
                metingtype=metingtype_deformatie,
            )
        metingen = MetingControle.objects.all()

        request = MagicMock()
        request.POST.getlist.return_value = [f.pk for f in metingen]

        model_admin.save_measurements(request, metingen)

        assert MetingControle.objects.count() == 0
        assert MetingHerzien.objects.count() == 4
        assert MetRefPuntenHerz.objects.count() == 12  # 3 ref points for 4 measurements

    def test_save_nap_measurements(self, client, model_admin, metingtype_nap):
        MetingControleFactory.create_batch(
            5, hoogtepunt=HoogtepuntFactory.create(type=Type.objects.get(pk=6)), metingtype=metingtype_nap
        )
        metingen = MetingControle.objects.all()

        request = Mock()
        request.POST.getlist.return_value = [f.pk for f in metingen]

        model_admin.save_measurements(request, metingen)

        assert MetingControle.objects.count() == 0
        assert MetingHerzien.objects.count() == len(metingen)

    def test_save_part_of_measurements(self, client, model_admin, metingtype_nap):
        MetingControleFactory.create_batch(
            5, hoogtepunt=HoogtepuntFactory.create(type=Type.objects.get(pk=6)), metingtype=metingtype_nap
        )
        metingen = MetingControle.objects.all()

        request = Mock()
        request.POST.getlist.return_value = [f.pk for f in metingen[:3]]

        model_admin.save_measurements(request, metingen)

        assert MetingControle.objects.count() == 2
        assert MetingHerzien.objects.count() == 3

