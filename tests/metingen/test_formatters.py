import pytest

from metingen.formatters import CORFormatClass, Meting, TCOFormatClass


@pytest.fixture
def metingencor():
    return [
        Meting("10389004", x=None, y=None, hoogte=-0.7349, sigmaz=0.0003),
        Meting("10381107", x=None, y=None, hoogte=1.4840, sigmaz=0.0004),
        Meting("10381105", x=None, y=None, hoogte=1.5192, sigmaz=0.0004),
        Meting("10381104", x=None, y=None, hoogte=1.5331, sigmaz=0.0004),
        Meting("10389005", x=None, y=None, hoogte=0.7761, sigmaz=0.0003),
    ]


@pytest.fixture
def metingentco():
    return [
        Meting(hoogtepunt="10389017", x="0.0000", y="0.0000", hoogte=0.0, sigmaz=None),
        Meting(hoogtepunt="10381465", x="0.0000", y="0.0000", hoogte=0.0, sigmaz=None),
        Meting(hoogtepunt="11189011", x="0.0000", y="0.0000", hoogte=0.0, sigmaz=None),
    ]


class TestFormats:
    def test_get_metingen_CORFormat(self, metingencor):
        with open("move3_files/metingen1.cor") as f:
            format = CORFormatClass()
            result, _ = format.get_metingen(f.read())

        assert result == metingencor

    def test_get_metingen_2(self):
        with open("move3_files/metingen2.cor") as f:
            format = CORFormatClass()
            dataset = format.create_dataset(f.read())

        assert len(dataset) == 17

    def test_get_metingen_TCOFormat(self, metingentco):
        with open("move3_files/raw.tco") as f:
            format = TCOFormatClass()
            result, header = format.get_metingen(f.read())
            print(header)
        assert result == metingentco
        assert header == "MOVE3 V4.5.1 TCO file\n$\nAD20\n$\nPROJECTION RD\n"

    def test_verrijktedata_TCOFormat(self):
        # TODO
        # import via admin "move3_files/raw.tco"
        # test verrijking -> x en y en hoogte niet leeg / error

        pass
