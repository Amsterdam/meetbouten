import pytest


from metingen.tco_loader import TCOFormatClass, MetingTCO
from metingen.models import MetingVerrijking

from django.urls import reverse


@pytest.fixture
def metingen():
    return [
        MetingTCO(
            hoogtepunt="10389017",
            x="0.0000",
            y="0.0000",
            hoogte=0.0,
            header="MOVE3 V4.5.1 TCO file\n$\nAD20\n$\nPROJECTION RD\n",
        ),
        MetingTCO(
            hoogtepunt="10381465",
            x="0.0000",
            y="0.0000",
            hoogte=0.0,
            header="MOVE3 V4.5.1 TCO file\n$\nAD20\n$\nPROJECTION RD\n",
        ),
        MetingTCO(
            hoogtepunt="11189011",
            x="0.0000",
            y="0.0000",
            hoogte=0.0,
            header="MOVE3 V4.5.1 TCO file\n$\nAD20\n$\nPROJECTION RD\n",
        ),
    ]


class TestTcoLoader:
    def test_get_metingen(self, metingen):
        with open("move3_files/raw.tco") as f:
            tco_format = TCOFormatClass()
            result = tco_format.get_metingen(f.read())

        assert result == metingen

    def test_verrijkte_data(self):

        # TODO
        # import via admin "move3_files/raw.tco"
        # test verrijking -> x en y en hoogte niet leeg / error

        pass
