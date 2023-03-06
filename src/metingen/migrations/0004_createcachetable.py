from django.core.management import call_command
from django.db import migrations


def createcachetable(apps, schema_editor):
    call_command('createcachetable')


class Migration(migrations.Migration):
    dependencies = [
        ('metingen', '0003_auto_20230215_1456'),
    ]

    operations = [
        migrations.RunPython(createcachetable),
    ]
