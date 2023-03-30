import pytest
from django.core.management import call_command
from django.db import connection

from metingen.models import (
    Grondslagpunt,
    Hoogtepunt,
    Meting,
    MetingHerzien,
    MetingReferentiepunt,
    MetRefPuntenHerz,
)


@pytest.mark.migration
@pytest.mark.django_db
def test_load_csv_data():
    call_command("load_csv_data")
    assert len(Meting.objects.all()) > 0
    assert len(MetingHerzien.objects.all()) > 0
    assert len(MetingReferentiepunt.objects.all()) > 0
    assert len(MetRefPuntenHerz.objects.all()) > 0
    assert len(Hoogtepunt.objects.all()) > 0
    assert len(Grondslagpunt.objects.all()) > 0

    # Check if sequence is set correctly
    for model in [MetingHerzien, Meting, Hoogtepunt, Grondslagpunt]:
        with connection.cursor() as cursor:
            query = f"""select nextval('{model._meta.db_table}_id_seq'::regclass)"""
            cursor.execute(query)
            value = cursor.fetchall()
            assert value[0][0] > 999
