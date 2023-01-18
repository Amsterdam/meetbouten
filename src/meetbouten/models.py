from django.db import models
from django.contrib.gis.db.models import PointField
from django.utils.html import mark_safe

from main import settings


class Type(models.Model):
    omschrijving = models.CharField(max_length=100, blank=True, null=True)
    soort = models.IntegerField()


class Grondslagpunt(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    order = models.IntegerField()
    inwindatum = models.DateField()
    vervaldatum = models.DateField()
    bron = models.IntegerField()
    wijze_inwinning = models.IntegerField()
    sigmax = models.FloatField(blank=True, null=True)
    sigmay = models.FloatField(blank=True, null=True)
    sigmaz = models.FloatField(blank=True, null=True)
    geom = PointField()
    omschrijving = models.CharField(max_length=100, blank=True, null=True)
    # picture = models.ImageField(upload_to="meetbouten_pictures/",
    #                             blank=True, null=True)
    #
    # def picture_tag(self):
    #     return mark_safe(f'<img src="{settings.MEDIA_URL}{self.picture}" width="50" height="50" />')
    # picture_tag.short_description = 'Picture'


class Hoogtepunt(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    agi_nummer = models.IntegerField()
    vervaldatum = models.DateField()
    merk = models.IntegerField()
    xmuur = models.FloatField(blank=True, null=True)
    ymuur = models.FloatField(blank=True, null=True)
    windr = models.CharField(max_length=10)
    sigmax = models.FloatField(blank=True, null=True)
    sigmay = models.FloatField(blank=True, null=True)
    omschrijving = models.CharField(max_length=100, blank=True, null=True)


class Bron(models.Model):
    omschrijving = models.CharField(max_length=100, blank=True, null=True)


class Meting(models.Model):
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE)
    inwindatum = models.DateField()
    wijze_inwinning = models.IntegerField()
    sigmaz = models.FloatField(blank=True, null=True)
    bro_id = models.IntegerField()


class Bouwblok(models.Model):
    aansluitpunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, related_name="bouwblok_aansluitpunt")
    controlepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, related_name="bouwblok_controlepunt")
    opmerking = models.CharField(max_length=100, blank=True, null=True)


class Referentiepunt(models.Model):
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    bouwblok = models.ForeignKey(Bouwblok, on_delete=models.CASCADE)


class Controlepunt(models.Model):
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    bouwblok = models.ForeignKey(Bouwblok, on_delete=models.CASCADE, related_name="controlepunt_bouwblok")


class Kringpunt(models.Model):
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE)
    bouwblok = models.ForeignKey(Bouwblok, on_delete=models.CASCADE)
    volgorde = models.IntegerField()
