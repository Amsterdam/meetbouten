from django.db import models


class WijzenInwinning(models.Model):
    class Meta:
        verbose_name_plural = "Wijzen inwinning"

    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=30)


class Type(models.Model):
    class Meta:
        verbose_name_plural = "Types"

    nummer = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=50)
    soort = models.IntegerField()


class Status(models.Model):
    class Meta:
        verbose_name_plural = "Statussen"

    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=30)


class Metingtype(models.Model):
    class Meta:
        verbose_name_plural = "Metingtypes"

    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=30)


class Merk(models.Model):
    class Meta:
        verbose_name_plural = "Merken"

    id = models.CharField(max_length=2, primary_key=True)
    omschrijving_verkort = models.CharField(max_length=30, db_column='omschr_verkort')
    omschrijving = models.CharField(max_length=256)


class Bron(models.Model):
    class Meta:
        verbose_name_plural = "Bronnen"

    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=20)
    doel = models.CharField(max_length=1)