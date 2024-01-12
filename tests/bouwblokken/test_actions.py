import datetime
from decimal import Decimal

import pytest

from bouwblokken.admin import BouwblokAdmin
from bouwblokken.factories import (
    BouwblokFactory,
    KringpuntFactory,
    ReferentiepuntFactory,
)
from bouwblokken.models import Bouwblok, Kringpunt
from metingen.factories import HoogtepuntFactory, MetingHerzFactory
from metingen.models import Hoogtepunt, MetingHerzien


@pytest.mark.django_db
class TestBouwblokActionsMixin:
    @pytest.mark.parametrize("report", ["get_report_history", "get_report_bouwblok"])
    def test_get_report_empty(self, report):
        self._assert_get_report(report)

    @pytest.mark.parametrize("report", ["get_report_history", "get_report_bouwblok"])
    def test_get_report_no_metingen(self, report):
        HoogtepuntFactory()
        BouwblokFactory()
        self._assert_get_report(report)

    @pytest.mark.parametrize("report", ["get_report_history", "get_report_bouwblok"])
    def test_get_report_with_meting(self, report):
        MetingHerzFactory(hoogtepunt=HoogtepuntFactory())
        BouwblokFactory()
        self._assert_get_report(report)

    @pytest.mark.parametrize("report", ["get_report_history", "get_report_bouwblok"])
    def test_get_report_with_multiple_metingen(self, report):
        hoogtepunten = HoogtepuntFactory.create_batch(2)
        BouwblokFactory()
        for hp in hoogtepunten:
            MetingHerzFactory.create_batch(3, hoogtepunt=hp)
        self._assert_get_report(report)

    def test_get_bouwblok_report(self):
        HoogtepuntFactory()
        bouwblok = BouwblokFactory()
        ReferentiepuntFactory.create_batch(
            2, bouwblok=bouwblok, hoogtepunt=HoogtepuntFactory()
        )
        ReferentiepuntFactory.create_batch(
            2, bouwblok=bouwblok, hoogtepunt=HoogtepuntFactory()
        )
        KringpuntFactory.create_batch(
            2, bouwblok=bouwblok, hoogtepunt=HoogtepuntFactory()
        )

        self._assert_get_report("get_report_bouwblok")

    def _assert_get_report(self, action_name):
        admin = BouwblokAdmin(Bouwblok, None)
        response = getattr(admin, action_name)(None, Bouwblok.objects.all())

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
                meting.id,
                hoogtepunt.nummer,
                meting.inwindatum,
                meting.hoogte,
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
        metingen = []
        for date, hoogte in zip(dates, hoogtes):
            meting = MetingHerzFactory(
                inwindatum=date, hoogte=hoogte, hoogtepunt=hoogtepunt
            )
            metingen.append(meting)

        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == [
            [
                bouwblok.nummer,
                metingen[0].id,
                hoogtepunt.nummer,
                datetime.date(year=1900, month=1, day=1),
                Decimal("2.0000"),
                Decimal("0.0000"),
                Decimal("0.0000"),
            ],
            [
                bouwblok.nummer,
                metingen[1].id,
                hoogtepunt.nummer,
                datetime.date(year=1900, month=1, day=2),
                Decimal("1.9000"),
                Decimal("-0.1000"),
                Decimal("-0.1000"),
            ],
            [
                bouwblok.nummer,
                metingen[2].id,
                hoogtepunt.nummer,
                datetime.date(year=1900, month=1, day=3),
                Decimal("1.5000"),
                Decimal("-0.4000"),
                Decimal("-0.5000"),
            ],
        ]

    def test_collect_data_multiple_bouwblokken(self):
        hoogtepunt_nrs = ["0000", "0001", "0002"]
        bouwblok_nrs = ["A", "B", "C"]
        dates = ["1900-01-01", "1900-01-02", "1900-01-03"]
        hoogtes = [2.0, 1.9, 1.5]
        metingen = []
        for hoo_nr, bou_nr, date, hoogte in zip(
            hoogtepunt_nrs, bouwblok_nrs, dates, hoogtes
        ):
            hoogtepunt = HoogtepuntFactory(nummer=hoo_nr)
            bouwblok = BouwblokFactory(
                nummer=bou_nr, controlepunt=hoogtepunt, aansluitpunt=hoogtepunt
            )
            KringpuntFactory(hoogtepunt=hoogtepunt, bouwblok=bouwblok)
            meting = MetingHerzFactory(
                inwindatum=date, hoogte=hoogte, hoogtepunt=hoogtepunt
            )
            metingen.append(meting)

        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == [
            [
                "A",
                metingen[0].id,
                "0000",
                datetime.date(year=1900, month=1, day=1),
                Decimal("2.0000"),
                Decimal("0.0000"),
                Decimal("0.0000"),
            ],
            [
                "B",
                metingen[1].id,
                "0001",
                datetime.date(year=1900, month=1, day=2),
                Decimal("1.9000"),
                Decimal("0.0000"),
                Decimal("0.0000"),
            ],
            [
                "C",
                metingen[2].id,
                "0002",
                datetime.date(year=1900, month=1, day=3),
                Decimal("1.5000"),
                Decimal("0.0000"),
                Decimal("0.0000"),
            ],
        ]

    def test_collect_data_complex_case(self):
        hoogtepunt_nrs = ["0000", "0001", "0002"]
        hoogtepunten = []
        for hp_nr in hoogtepunt_nrs:
            hoogtepunten.append(HoogtepuntFactory(nummer=hp_nr))
        bouwblok = BouwblokFactory()
        for hp in hoogtepunten:
            KringpuntFactory(hoogtepunt=hp, bouwblok=bouwblok)

        meting1 = MetingHerzFactory(
            inwindatum="1900-01-03", hoogte=2, hoogtepunt=hoogtepunten[2]
        )
        meting2 = MetingHerzFactory(
            inwindatum="1900-01-02", hoogte=3, hoogtepunt=hoogtepunten[2]
        )
        meting3 = MetingHerzFactory(
            inwindatum="1900-01-01", hoogte=3.1, hoogtepunt=hoogtepunten[2]
        )
        meting4 = MetingHerzFactory(
            inwindatum="1900-01-15", hoogte=5, hoogtepunt=hoogtepunten[0]
        )
        meting5 = MetingHerzFactory(
            inwindatum="1900-01-15", hoogte=3, hoogtepunt=hoogtepunten[1]
        )
        meting6 = MetingHerzFactory(
            inwindatum="1900-01-16", hoogte=2.5, hoogtepunt=hoogtepunten[1]
        )

        admin = BouwblokAdmin(Bouwblok, None)
        data = admin.collect_data(Bouwblok.objects.all())
        assert data == [
            [
                bouwblok.nummer,
                meting4.id,
                hoogtepunten[0].nummer,
                datetime.date(year=1900, month=1, day=15),
                Decimal("5.0000"),
                Decimal("0.0000"),
                Decimal("0.0000"),
            ],
            [
                bouwblok.nummer,
                meting5.id,
                hoogtepunten[1].nummer,
                datetime.date(year=1900, month=1, day=15),
                Decimal("3.0000"),
                Decimal("0.0000"),
                Decimal("0.0000"),
            ],
            [
                bouwblok.nummer,
                meting6.id,
                hoogtepunten[1].nummer,
                datetime.date(year=1900, month=1, day=16),
                Decimal("2.5000"),
                Decimal("-0.5000"),
                Decimal("-0.5000"),
            ],
            [
                bouwblok.nummer,
                meting3.id,
                hoogtepunten[2].nummer,
                datetime.date(year=1900, month=1, day=1),
                Decimal("3.1000"),
                Decimal("0.0000"),
                Decimal("0.0000"),
            ],
            [
                bouwblok.nummer,
                meting2.id,
                hoogtepunten[2].nummer,
                datetime.date(year=1900, month=1, day=2),
                Decimal("3.0000"),
                Decimal("-0.1000"),
                Decimal("-0.1000"),
            ],
            [
                bouwblok.nummer,
                meting1.id,
                hoogtepunten[2].nummer,
                datetime.date(year=1900, month=1, day=3),
                Decimal("2.0000"),
                Decimal("-1.0000"),
                Decimal("-1.1000"),
            ],
        ]

    def teardown_method(self, _):
        """Reset the database after each test"""
        MetingHerzien.objects.all().delete()
        Kringpunt.objects.all().delete()
        Bouwblok.objects.all().delete()
        Hoogtepunt.objects.all().delete()
