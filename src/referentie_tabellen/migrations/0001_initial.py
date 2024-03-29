# Generated by Django 3.2.16 on 2023-02-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bron",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("omschrijving", models.CharField(max_length=20)),
                ("doel", models.CharField(max_length=1)),
            ],
            options={
                "verbose_name_plural": "Bronnen",
            },
        ),
        migrations.CreateModel(
            name="Merk",
            fields=[
                (
                    "id",
                    models.CharField(max_length=2, primary_key=True, serialize=False),
                ),
                (
                    "omschrijving_verkort",
                    models.CharField(db_column="omschr_verkort", max_length=30),
                ),
                ("omschrijving", models.CharField(max_length=256)),
            ],
            options={
                "verbose_name_plural": "Merken",
            },
        ),
        migrations.CreateModel(
            name="Metingtype",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("omschrijving", models.CharField(max_length=30)),
            ],
            options={
                "verbose_name_plural": "Metingtypes",
            },
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("omschrijving", models.CharField(max_length=30)),
            ],
            options={
                "verbose_name_plural": "Statussen",
            },
        ),
        migrations.CreateModel(
            name="Type",
            fields=[
                ("nummer", models.AutoField(primary_key=True, serialize=False)),
                ("omschrijving", models.CharField(max_length=50)),
                ("soort", models.IntegerField()),
            ],
            options={
                "verbose_name_plural": "Types",
            },
        ),
        migrations.CreateModel(
            name="WijzenInwinning",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("omschrijving", models.CharField(max_length=30)),
            ],
            options={
                "verbose_name_plural": "Wijzen inwinning",
            },
        ),
    ]
