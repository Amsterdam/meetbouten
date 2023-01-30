from django.db import models
from django.contrib.gis.db.models import PointField
from django.utils.html import mark_safe

from main import settings


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

    id = models.AutoField(primary_key=True)
    omschrijving_verkort = models.CharField(max_length=30)
    omschrijving = models.CharField(max_length=256)


class Bron(models.Model):
    class Meta:
        verbose_name_plural = "Bronnen"

    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=20)
    doel = models.CharField(max_length=1)


class Hoogtepunt(models.Model):
    class Meta:
        verbose_name_plural = "Hoogtepunten"

    id = models.AutoField(primary_key=True)
    nummer = models.IntegerField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column="typ_nummer")
    agi_nummer = models.CharField(max_length=8)
    vervaldatum = models.DateField(null=True)
    omschrijving = models.CharField(max_length=100, blank=True, null=True)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE, db_column="mer_id")
    xmuur = models.FloatField(blank=True, null=True)
    ymuur = models.FloatField(blank=True, null=True)
    windr = models.CharField(max_length=10)
    sigmax = models.FloatField(blank=True, null=True)
    sigmay = models.FloatField(blank=True, null=True)
    geom = PointField(srid=28992)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, db_column="sta_id")
    orde = models.IntegerField()


class Grondslagpunt(models.Model):
    class Meta:
        verbose_name_plural = "Gronslagpunten"

    id = models.AutoField(primary_key=True)
    nummer = models.CharField(max_length=8)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column="typ_nummer")
    rdnummer = models.DecimalField(max_digits=8, decimal_places=0)
    orde = models.DecimalField(max_digits=1, decimal_places=0)
    inwindatum = models.DateField()
    vervaldatum = models.DateField()
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    wijze_inwinning = models.DecimalField(max_digits=1, decimal_places=0)
    sigmax = models.DecimalField(max_digits=4, decimal_places=2)
    sigmay = models.DecimalField(max_digits=4, decimal_places=2)
    sigmaz = models.DecimalField(max_digits=4, decimal_places=2)
    # geom = PointField()
    omschrijving = models.CharField(max_length=256, blank=True, null=True)
    z = models.IntegerField()
    # picture = models.ImageField(upload_to="meetbouten_pictures/",
    #                             blank=True, null=True)
    #
    # def picture_tag(self):
    #     return mark_safe(f'<img src="{settings.MEDIA_URL}{self.picture}" width="50" height="50" />')
    # picture_tag.short_description = 'Picture'


class MetingHerzien(models.Model):
    class Meta:
        verbose_name_plural = "Metingherzieningen"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    inwindatum = models.DateField()
    wijze_inwinning = models.IntegerField()
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4)
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    hoogte = models.IntegerField()
    metingtype = models.ForeignKey(Metingtype, on_delete=models.CASCADE, db_column="myt_id")


class Meting(models.Model):
    class Meta:
        verbose_name_plural = "Metingen"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    inwindatum = models.DateField()
    wijze_inwinning = models.IntegerField()
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4)
    bro_id = models.IntegerField()
    hoogte = models.IntegerField()
    metingtype = models.ForeignKey(Metingtype, on_delete=models.CASCADE, db_column="myt_id")


class Bouwblok(models.Model):
    class Meta:
        verbose_name_plural = "Bouwblokken"

    nummer = models.CharField(max_length=8, primary_key=True)
    aansluitpunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, related_name="bouwblok_aansluitpunt", db_column="aansluitpnt"
    )
    controlepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, related_name="bouwblok_controlepunt", db_column="controlepnt"
    )
    opmerking = models.CharField(max_length=256, blank=True, null=True)


class Controlepunt(models.Model):
    class Meta:
        verbose_name_plural = "Controlpunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    bouwblok = models.ForeignKey(
        Bouwblok, on_delete=models.CASCADE, related_name="controlepunt_bouwblok", db_column="bou_nummer"
    )


class Referentiepunt(models.Model):
    class Meta:
        verbose_name_plural = "Referentiepunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    bouwblok = models.ForeignKey(Bouwblok, on_delete=models.CASCADE, db_column="bou_nummer")


class MetingReferentiepunt(models.Model):
    class Meta:
        verbose_name_plural = "Meting referentiepunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    meting = models.ForeignKey(Meting, on_delete=models.CASCADE, db_column="met_id")


class MetRefPuntenHerz(models.Model):
    class Meta:
        verbose_name = "Meting referentiepunten herziening"
        verbose_name_plural = "Meting referentiepunten herzieningen"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    meting = models.ForeignKey(Meting, on_delete=models.CASCADE, db_column="met_id")


class Kringpunt(models.Model):
    class Meta:
        verbose_name_plural = "Kringpunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    bouwblok = models.ForeignKey(Bouwblok, on_delete=models.CASCADE, db_column="bou_nummer")
    volgorde = models.IntegerField()
