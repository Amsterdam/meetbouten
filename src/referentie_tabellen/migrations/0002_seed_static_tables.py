from django.db import migrations

from referentie_tabellen.referentie_waardes import (
    bronnen,
    merken,
    metingtypen,
    statussen,
    types,
    wijzen_inwinning,
)


def seed_tables(apps, schema_editor):
    """
    Seed the static tables with the data from the referentie_waardes.py file
    """
    data_mapping = [
        {"model": "WijzenInwinning", "values": wijzen_inwinning},
        {"model": "Type", "values": types},
        {"model": "Status", "values": statussen},
        {"model": "Metingtype", "values": metingtypen},
        {"model": "Merk", "values": merken},
        {"model": "Bron", "values": bronnen},
    ]
    for mapping in data_mapping:
        model = apps.get_model("referentie_tabellen", mapping["model"])
        data = [model(**value._asdict()) for value in mapping["values"]]
        model.objects.bulk_create(data)


class Migration(migrations.Migration):
    """
    This migration seeds the static data tables
    """

    dependencies = [
        ("metingen", "0001_initial"),
        ("referentie_tabellen", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(code=seed_tables, reverse_code=migrations.RunPython.noop)
    ]
