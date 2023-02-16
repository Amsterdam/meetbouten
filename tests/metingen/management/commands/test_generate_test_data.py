import pytest
from django.core.management import call_command

from metingen.models import Meting, MetingHerzien, MetingReferentiepunt, MetRefPuntenHerz


@pytest.mark.django_db
def test_load_csv_data():
    call_command('generate_test_data', num=10)
    assert len(Meting.objects.all()) == 10
    assert len(MetingHerzien.objects.all()) == 10
    assert len(MetingReferentiepunt.objects.all()) == 10
    assert len(MetRefPuntenHerz.objects.all()) == 10
