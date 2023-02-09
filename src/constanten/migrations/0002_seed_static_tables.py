from django.db import migrations

from constanten.constants import wijzen_inwinning, types, statussen, metingtypen, merken, bronnen


def seed_tables(apps, schema_editor):
    """
    Seed the static tables with the data from the constants.py file
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
        model = apps.get_model('constanten', mapping["model"])
        data = [model(**value._asdict()) for value in mapping["values"]]
        model.objects.bulk_create(data)


class Migration(migrations.Migration):
    """
    This migration seeds the static data tables
    """

    dependencies = [
        ('metingen', '0001_initial'),
        ('constanten', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(
            code=seed_tables,
            reverse_code=migrations.RunPython.noop)
    ]
