# Generated by Django 3.2.18 on 2023-03-13 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metingen", "0006_hoogtepunt_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="MetingVerrijking",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("x", models.DecimalField(decimal_places=4, max_digits=10)),
                ("y", models.DecimalField(decimal_places=4, max_digits=10)),
                ("hoogte", models.FloatField(blank=True, null=True)),
                ("inwindatum", models.DateField(blank=True, null=True)),
                (
                    "c1",
                    models.DecimalField(decimal_places=4, default=1.0, max_digits=6),
                ),
                (
                    "c2",
                    models.DecimalField(decimal_places=4, default=1.0, max_digits=6),
                ),
                (
                    "c3",
                    models.DecimalField(decimal_places=4, default=0.0, max_digits=6),
                ),
                ("header", models.CharField(max_length=60)),
                (
                    "hoogtepunt",
                    models.ForeignKey(
                        db_column="hoo_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="metingen.hoogtepunt",
                    ),
                ),
            ],
            options={
                "verbose_name": "Meting [verrijking]",
                "verbose_name_plural": "Metingen [verrijking]",
            },
        ),
    ]
