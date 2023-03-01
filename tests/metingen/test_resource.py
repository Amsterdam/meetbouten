import pytest

from metingen.resource import CORFormat


@pytest.fixture
def metingen():
    return [
        ("10389004", "0.7349", "0.0003"),
        ("10381107", "1.4840", "0.0004"),
        ("10381105", "1.5192", "0.0004"),
        ("10381104", "1.5331", "0.0004"),
        ("10389005", "0.7761", "0.0003"),
    ]


class TestCorLoader:
    def test_get_metingen(self, metingen):
        with open("move3_files/metingen1.cor") as f:
            cor_format = CORFormat()
            new_stream = cor_format.reformat_cor_to_csv(f.read())

        expected = "hoogtepunt,hoogte,sigmaz\n"
        for meting in metingen:
            expected += ",".join([str(m) for m in meting]) + "\n"
        assert expected == new_stream

    def test_get_metingen_2(self):
        with open("move3_files/metingen2.cor") as f:
            cor_format = CORFormat()
            new_stream = cor_format.reformat_cor_to_csv(f.read())

        assert len(new_stream.splitlines()) == 18
