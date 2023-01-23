from django.db import models
from django.contrib.gis.db.models import PointField
from django.utils.html import mark_safe

from main import settings


class WijzenInwinning(models.Model):
    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=30)


class Type(models.Model):
    nummer = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=50)
    soort = models.IntegerField()


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=30)


class Metingtype(models.Model):
    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=30)


class Merk(models.Model):
    id = models.AutoField(primary_key=True)
    omschrijving_verkort = models.CharField(max_length=30)
    omschrijving = models.CharField(max_length=256)


class Bron(models.Model):
    id = models.AutoField(primary_key=True)
    omschrijving = models.CharField(max_length=20)
    doel = models.CharField(max_length=1)


class Hoogtepunt(models.Model):
    id = models.AutoField(primary_key=True)
    nummer = models.IntegerField()
    typ_nummer = models.ForeignKey(Type, on_delete=models.CASCADE)
    agi_nummer = models.IntegerField()
    vervaldatum = models.DateField()
    omschrijving = models.CharField(max_length=100, blank=True, null=True)
    mer_id = models.ForeignKey(Merk, on_delete=models.CASCADE)
    xmuur = models.FloatField(blank=True, null=True)
    ymuur = models.FloatField(blank=True, null=True)
    windr = models.CharField(max_length=10)
    sigmax = models.FloatField(blank=True, null=True)
    sigmay = models.FloatField(blank=True, null=True)
    # geom = PointField()
    sta_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    orde = models.IntegerField()


class Grondslagpunt(models.Model):
    id = models.AutoField(primary_key=True)
    nummer = models.CharField(max_length=8)
    typ_nummer = models.ForeignKey(Type, on_delete=models.CASCADE)
    rdnummer = models.DecimalField(max_digits=8, decimal_places=0)
    orde = models.DecimalField(max_digits=1, decimal_places=0)
    inwindatum = models.DateField()
    vervaldatum = models.DateField()
    bro_id = models.ForeignKey(Bron, on_delete=models.CASCADE)
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
    id = models.AutoField(primary_key=True)
    hoo_id = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    inwindatum = models.DateField()
    wijze_inwinning = models.IntegerField()
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4)
    bro_id = models.IntegerField()
    hoogte = models.IntegerField()
    myt_id = models.ForeignKey(Metingtype, on_delete=models.CASCADE)


class Meting(models.Model):
    id = models.AutoField(primary_key=True)
    hoo_id = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    inwindatum = models.DateField()
    wijze_inwinning = models.IntegerField()
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4)
    bro_id = models.IntegerField()
    hoogte = models.IntegerField()
    myt_id = models.ForeignKey(Metingtype, on_delete=models.CASCADE)


class Bouwblok(models.Model):
    nummer = models.CharField(max_length=8, primary_key=True)
    aansluitpnt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, related_name="bouwblok_aansluitpunt")
    controlepnt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, related_name="bouwblok_controlepunt")
    opmerking = models.CharField(max_length=256, blank=True, null=True)


class Controlepunt(models.Model):
    id = models.AutoField(primary_key=True)
    hoo_id = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    bou_nummer = models.ForeignKey(Bouwblok, on_delete=models.CASCADE, related_name="controlepunt_bouwblok")


class Referentiepunt(models.Model):
    id = models.AutoField(primary_key=True)
    hoo_id = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    bou_nummer = models.ForeignKey(Bouwblok, on_delete=models.CASCADE)


class MetingReferentiepunt(models.Model):
    id = models.AutoField(primary_key=True)
    hoo_id = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    met_id = models.ForeignKey(Meting, on_delete=models.CASCADE)


class MetRefPuntenHerz(models.Model):
    id = models.AutoField(primary_key=True)
    met_id = models.ForeignKey(Meting, on_delete=models.CASCADE)
    hoo_id = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)


class Kringpunt(models.Model):
    id = models.AutoField(primary_key=True)
    hoo_id = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    bou_nummer = models.ForeignKey(Bouwblok, on_delete=models.CASCADE)
    volgorde = models.IntegerField()
