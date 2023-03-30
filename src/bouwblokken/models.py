from django.db import models

from metingen.models import Hoogtepunt


class Bouwblok(models.Model):
    class Meta:
        verbose_name_plural = "Bouwblokken"

    nummer = models.CharField(max_length=8, primary_key=True)
    aansluitpunt = models.ForeignKey(
        Hoogtepunt,
        on_delete=models.CASCADE,
        related_name="bouwblok_aansluitpunt",
        db_column="aansluitpnt",
    )
    controlepunt = models.ForeignKey(
        Hoogtepunt,
        on_delete=models.CASCADE,
        related_name="bouwblok_controlepunt",
        db_column="controlepnt",
    )
    opmerking = models.CharField(max_length=256, blank=True, null=True)


class Controlepunt(models.Model):
    class Meta:
        verbose_name_plural = "Controlepunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    bouwblok = models.ForeignKey(
        Bouwblok,
        on_delete=models.CASCADE,
        related_name="controlepunt_bouwblok",
        db_column="bou_nummer",
    )


class Referentiepunt(models.Model):
    class Meta:
        verbose_name_plural = "Referentiepunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    bouwblok = models.ForeignKey(
        Bouwblok, on_delete=models.CASCADE, db_column="bou_nummer"
    )


class Kringpunt(models.Model):
    class Meta:
        verbose_name_plural = "Kringpunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    bouwblok = models.ForeignKey(
        Bouwblok, on_delete=models.CASCADE, db_column="bou_nummer"
    )
    volgorde = models.IntegerField()
