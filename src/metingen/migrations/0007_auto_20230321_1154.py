# Generated by Django 3.2.18 on 2023-03-21 11:54

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metingen', '0006_hoogtepunt_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoogtepunt',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, srid=28992),
        ),
        migrations.AlterField(
            model_name='hoogtepunt',
            name='nummer',
            field=models.CharField(blank=True, max_length=8, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
    ]
