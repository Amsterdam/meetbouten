import pytest
from metingen.factories import HoogtepuntFactory
from metingen.hoogtepunt_nummer_generator import HoogtepuntNummerGenerator, Kaartblad
from referentie_tabellen.models import Type


@pytest.mark.django_db
class TestHoogtepuntNummerGenerator:
    def test_load_bladnummers(self):
        generator = HoogtepuntNummerGenerator()

        bladen = generator.load_bladnummers()

        assert len(bladen) == 576

    def test_load_bladnummers_subset(self):
        generator = HoogtepuntNummerGenerator()

        bladen = generator.load_bladnummers(filename="kaartbladen-test.csv")

        assert bladen == [
            Kaartblad(bladnr="101", xmin=117650, ymin=487000, xmax=118600, ymax=487750),
            Kaartblad(bladnr="102", xmin=118600, ymin=487000, xmax=119550, ymax=487750),
            Kaartblad(bladnr="103", xmin=119550, ymin=487000, xmax=120500, ymax=487750),
            Kaartblad(bladnr="104", xmin=120500, ymin=487000, xmax=121450, ymax=487750),
            Kaartblad(bladnr="105", xmin=121450, ymin=487000, xmax=122400, ymax=487750),
        ]

    @pytest.mark.parametrize(
        "bladnr,coordinates",
        [
            ("649", (118000, 477000)),
            ("112", (121000, 486500)),
            ("101", (118000, 487700)),
            ("964", (117000, 488000)),
            ("000", (0, 0)),
        ],
    )
    def test_get_bladnr(self, bladnr, coordinates):
        generator = HoogtepuntNummerGenerator()
        generator.load_bladnummers()

        x, y = coordinates
        result = generator.get_bladnr(x=x, y=y)

        assert bladnr == result

    @pytest.mark.parametrize(
        "boutnaam,nummer",
        [
            ("Deformatiebout", 1),
            ("NAP-bout", 0),
            ("Referentiebout", 9),
            ("Ondergronds merk", 8),
        ],
    )
    def test_get_bouttype_nr(self, boutnaam, nummer):
        generator = HoogtepuntNummerGenerator()

        bouttype_nr = Type.objects.get(omschrijving=boutnaam).nummer
        result = generator.get_bouttype_nr(bouttype_nr)

        assert result == str(nummer)

    def test_get_volgnr_empty(self):
        generator = HoogtepuntNummerGenerator()

        result = generator.get_volgnr(nummer="12348")

        assert result == "001"

    @pytest.mark.parametrize(
        "start_nummer,expected",
        [
            ("12348", "001"),
            ("93486", "122"),
            ("83486", "049"),
            ("23786", "284"),
        ],
    )
    def test_get_volgnr(self, start_nummer, expected):
        for nr in ["93486121", "93486002", "93486015", "23786283", "83486012", "83486002", "83486048"]:
            HoogtepuntFactory(nummer=nr)
        generator = HoogtepuntNummerGenerator()

        result = generator.get_volgnr(nummer=start_nummer)

        assert result == expected

    def test_generate(self):
        hoogtepunt = HoogtepuntFactory(
            geom="POINT(114700 487100)",
            type=Type.objects.get(omschrijving="Deformatiebout"),
        )
        generator = HoogtepuntNummerGenerator()
        generator.load_bladnummers()

        result = generator.generate(hoogtepunt)

        assert result == "80581001"

    def test_generate_multiple(self):
        hoogtepunten = [HoogtepuntFactory(
            geom="POINT(114700 487100)",
            type=Type.objects.get(omschrijving="Deformatiebout"),
            nummer=None
        ) for i in range(10)]
        generator = HoogtepuntNummerGenerator()
        generator.load_bladnummers()

        result = generator.generate(hoogtepunten[0])

        assert result == "80581011"
