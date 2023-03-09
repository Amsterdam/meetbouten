import pytest

from metingen.cor_loader import CORFormatClass, Meting


@pytest.fixture
def metingen():
    return [
        Meting("10389004", hoogte=0.7349, sigmaz=0.0003),
        Meting("10381107", hoogte=1.4840, sigmaz=0.0004),
        Meting("10381105", hoogte=1.5192, sigmaz=0.0004),
        Meting("10381104", hoogte=1.5331, sigmaz=0.0004),
        Meting("10389005", hoogte=0.7761, sigmaz=0.0003),
    ]


class TestCorLoader:
    def test_get_metingen(self, metingen):
        with open("move3_files/metingen1.cor") as f:
            cor_format = CORFormatClass()
            result = cor_format.get_metingen(f.read())

        assert result == metingen

    def test_get_metingen_2(self):
        with open("move3_files/metingen2.cor") as f:
            cor_format = CORFormatClass()
            dataset = cor_format.create_dataset(f.read())

        assert len(dataset) == 17
