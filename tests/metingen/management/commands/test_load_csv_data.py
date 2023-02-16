import pytest
from django.core.management import call_command

from metingen.models import Meting, MetingHerzien, MetingReferentiepunt, MetRefPuntenHerz


@pytest.mark.migration
@pytest.mark.django_db
def test_load_csv_data():
    call_command('load_csv_data')
    assert len(Meting.objects.all()) > 0
    assert len(MetingHerzien.objects.all()) > 0
    assert len(MetingReferentiepunt.objects.all()) > 0
    assert len(MetRefPuntenHerz.objects.all()) > 0
