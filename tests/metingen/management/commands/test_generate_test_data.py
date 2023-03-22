import pytest
from django.core.management import call_command

from bouwblokken.models import Bouwblok, Kringpunt
from metingen.models import Meting, MetingHerzien, MetingReferentiepunt, MetRefPuntenHerz


@pytest.mark.django_db
class TestGenerateTestData:
    def test_load_csv_data(self):
        call_command('generate_test_data', num=10)
        assert len(Meting.objects.all()) == 10
        assert len(MetingHerzien.objects.all()) == 10
        assert len(MetingReferentiepunt.objects.all()) == 10
        assert len(MetRefPuntenHerz.objects.all()) == 10

    def teardown_method(self, _):
        """ Reset the database after each test """
        Bouwblok.objects.all().delete()
        Kringpunt.objects.all().delete()