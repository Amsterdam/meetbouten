import datetime

import pytest

from bouwblokken.admin import BouwblokAdmin
from bouwblokken.factories import BouwblokFactory, KringpuntFactory
from bouwblokken.models import Bouwblok, Kringpunt
from metingen.factories import HoogtepuntFactory, MetingHerzFactory
from metingen.models import Hoogtepunt, MetingHerzien


@pytest.mark.django_db
class TestBouwblokActionsMixin:
    def test_get_report_empty(self):
        self._assert_get_report()

    def test_get_report_no_metingen(self):
        HoogtepuntFactory()
        BouwblokFactory()
        self._assert_get_report()

    def test_get_report_with_meting(self):
        MetingHerzFactory(hoogtepunt=HoogtepuntFactory())
        BouwblokFactory()
        self._assert_get_report()

    def test_get_report_with_metingen(self):
        hoogtepunten = HoogtepuntFactory.create_batch(2)
        BouwblokFactory()
        for hp in hoogtepunten:
            MetingHerzFactory.create_batch(3, hoogtepunt=hp)
        self._assert_get_report()

    def _assert_get_report(self):
        admin = BouwblokAdmin(Bouwblok, None)
        response = admin.get_report(None, Bouwblok.objects.all())

        assert response.status_code == 200
        assert (
            response.headers["Content-Type"]
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        assert response.content.startswith(b"PK\x03")

    def test_collect_data_empty(self):
        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == []

    def test_collect_data_hoogtepunt_without_measurement(self):
        hoogtepunt = HoogtepuntFactory()
        BouwblokFactory()
        KringpuntFactory(hoogtepunt=hoogtepunt)

        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == []

    def test_collect_data_single_measurement(self):
        hoogtepunt = HoogtepuntFactory()
        bouwblok = BouwblokFactory()
        KringpuntFactory(hoogtepunt=hoogtepunt, bouwblok=bouwblok)
        meting = MetingHerzFactory(hoogtepunt=hoogtepunt)

        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == [
            [
                bouwblok.nummer,
                hoogtepunt.nummer,
                meting.inwindatum,
                float(meting.hoogte),
                0.0,
                0.0,
            ]
        ]

    def test_collect_data_multiple_measurements(self):
        hoogtepunt = HoogtepuntFactory()
        bouwblok = BouwblokFactory()
        KringpuntFactory(bouwblok=bouwblok, hoogtepunt=hoogtepunt)
        dates = ["1900-01-01", "1900-01-02", "1900-01-03"]
        hoogtes = [2.0, 1.9, 1.5]
        for date, hoogte in zip(dates, hoogtes):
            MetingHerzFactory(inwindatum=date, hoogte=hoogte, hoogtepunt=hoogtepunt)

        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == [
            [
                bouwblok.nummer,
                hoogtepunt.nummer,
                datetime.date(year=1900, month=1, day=1),
                2,
                0.0,
                0.0,
            ],
            [
                bouwblok.nummer,
                hoogtepunt.nummer,
                datetime.date(year=1900, month=1, day=2),
                1.9,
                -0.1,
                -0.1,
            ],
            [
                bouwblok.nummer,
                hoogtepunt.nummer,
                datetime.date(year=1900, month=1, day=3),
                1.5,
                -0.4,
                -0.5,
            ],
        ]

    def test_collect_data_multiple_bouwblokken(self):
        hoogtepunt_nrs = ["0000", "0001", "0002"]
        bouwblok_nrs = ["A", "B", "C"]
        dates = ["1900-01-01", "1900-01-02", "1900-01-03"]
        hoogtes = [2.0, 1.9, 1.5]
        for hoo_nr, bou_nr, date, hoogte in zip(
            hoogtepunt_nrs, bouwblok_nrs, dates, hoogtes
        ):
            hoogtepunt = HoogtepuntFactory(nummer=hoo_nr)
            bouwblok = BouwblokFactory(
                nummer=bou_nr, controlepunt=hoogtepunt, aansluitpunt=hoogtepunt
            )
            KringpuntFactory(hoogtepunt=hoogtepunt, bouwblok=bouwblok)
            MetingHerzFactory(inwindatum=date, hoogte=hoogte, hoogtepunt=hoogtepunt)

        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == [
            ["A", "0000", datetime.date(year=1900, month=1, day=1), 2, 0.0, 0.0],
            ["B", "0001", datetime.date(year=1900, month=1, day=2), 1.9, 0.0, 0.0],
            ["C", "0002", datetime.date(year=1900, month=1, day=3), 1.5, 0.0, 0.0],
        ]

    def test_collect_data_complex_case(self):
        hoogtepunt_nrs = ["0000", "0001", "0002"]
        hoogtepunten = []
        for hp_nr in hoogtepunt_nrs:
            hoogtepunten.append(HoogtepuntFactory(nummer=hp_nr))
        bouwblok = BouwblokFactory()
        for hp in hoogtepunten:
            KringpuntFactory(hoogtepunt=hp, bouwblok=bouwblok)

        MetingHerzFactory(inwindatum="1900-01-03", hoogte=2, hoogtepunt=hoogtepunten[2])
        MetingHerzFactory(inwindatum="1900-01-02", hoogte=3, hoogtepunt=hoogtepunten[2])
        MetingHerzFactory(
            inwindatum="1900-01-01", hoogte=3.1, hoogtepunt=hoogtepunten[2]
        )
        MetingHerzFactory(inwindatum="1900-01-15", hoogte=5, hoogtepunt=hoogtepunten[0])
        MetingHerzFactory(inwindatum="1900-01-15", hoogte=3, hoogtepunt=hoogtepunten[1])
        MetingHerzFactory(
            inwindatum="1900-01-16", hoogte=2.5, hoogtepunt=hoogtepunten[1]
        )

        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == [
            [
                bouwblok.nummer,
                hoogtepunten[0].nummer,
                datetime.date(year=1900, month=1, day=15),
                5.0,
                0.0,
                0.0,
            ],
            [
                bouwblok.nummer,
                hoogtepunten[1].nummer,
                datetime.date(year=1900, month=1, day=15),
                3.0,
                0.0,
                0.0,
            ],
            [
                bouwblok.nummer,
                hoogtepunten[1].nummer,
                datetime.date(year=1900, month=1, day=16),
                2.5,
                -0.5,
                -0.5,
            ],
            [
                bouwblok.nummer,
                hoogtepunten[2].nummer,
                datetime.date(year=1900, month=1, day=1),
                3.1,
                0.0,
                0.0,
            ],
            [
                bouwblok.nummer,
                hoogtepunten[2].nummer,
                datetime.date(year=1900, month=1, day=2),
                3.0,
                -0.1,
                -0.1,
            ],
            [
                bouwblok.nummer,
                hoogtepunten[2].nummer,
                datetime.date(year=1900, month=1, day=3),
                2.0,
                -1,
                -1.1,
            ],
        ]

    def teardown_method(self, _):
        """Reset the database after each test"""
        MetingHerzien.objects.all().delete()
        Kringpunt.objects.all().delete()
        Bouwblok.objects.all().delete()
        Hoogtepunt.objects.all().delete()
