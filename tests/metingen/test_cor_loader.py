import pytest
from model_bakery import baker

from metingen.cor_loader import CORLoader, Meting
from metingen.factories import HoogtepuntFactory
from metingen.models import MetingControle, Hoogtepunt


@pytest.fixture
def metingen():
    return [
        Meting(puntnummer="10389004", x=120033.6, y=487446.1, z=0.7349),
        Meting(puntnummer="10381107", x=120019.0, y=487514.0, z=1.484),
        Meting(puntnummer="10381105", x=120009.0, y=487518.0, z=1.5192),
        Meting(puntnummer="10381104", x=120004.0, y=487520.0, z=1.5331),
        Meting(puntnummer="10389005", x=119958.7, y=487486.0, z=0.7761),
    ]


class TestCorLoader:
    def test_get_metingen(self, metingen):
        cor_loader = CORLoader("move3_files/metingen1.cor")
        cor_loader.get_data()
        assert metingen == cor_loader.get_metingen()

    def test_get_metingen_2(self):
        cor_loader = CORLoader("move3_files/metingen2.cor")
        cor_loader.get_data()
        metingen = cor_loader.get_metingen()
        assert len(metingen) == 17

    @pytest.mark.django_db
    def test_load_metingen_into_db(self, metingen):
        cor_loader = CORLoader("")
        # Create hoogtepunt objects
        for m in metingen:
            HoogtepuntFactory(nummer=m.puntnummer)

        cor_loader.load_metingen_into_db(metingen)

        metingen_db = MetingControle.objects.all()
        assert len(metingen_db) == len(metingen)

    @pytest.mark.django_db
    def test_load(self, metingen):
        cor_loader = CORLoader("move3_files/metingen1.cor")
        # Create hoogtepunt objects
        for m in metingen:
            HoogtepuntFactory(nummer=m.puntnummer)

        cor_loader.load()

        metingen_db = MetingControle.objects.all()
        assert len(metingen_db) == len(metingen)
