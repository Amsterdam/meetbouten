from django.db import models
from django.contrib.gis.db.models import PointField
from constanten.models import Type, Status, Metingtype, Merk, Bron, WijzenInwinning


class Hoogtepunt(models.Model):
    class Meta:
        verbose_name_plural = "Hoogtepunten"

    id = models.AutoField(primary_key=True)
    nummer = models.CharField(max_length=8)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column="typ_nummer")
    agi_nummer = models.CharField(max_length=8, null=True)
    vervaldatum = models.DateField(null=True)
    omschrijving = models.CharField(max_length=256, blank=True, null=True)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE, db_column="mer_id")
    xmuur = models.FloatField(blank=True, null=True)
    ymuur = models.FloatField(blank=True, null=True)
    windr = models.CharField(max_length=2)
    sigmax = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    sigmay = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    geom = PointField(srid=28992)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, db_column="sta_id", null=True)
    orde = models.IntegerField(null=True)


class Grondslagpunt(models.Model):
    class Meta:
        verbose_name_plural = "Gronslagpunten"

    id = models.AutoField(primary_key=True)
    nummer = models.CharField(max_length=8)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column="typ_nummer")
    rdnummer = models.DecimalField(max_digits=8, decimal_places=0, null=True)
    orde = models.DecimalField(max_digits=1, decimal_places=0)
    inwindatum = models.DateField()
    vervaldatum = models.DateField(null=True)
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    wijze_inwinning = models.ForeignKey(WijzenInwinning, on_delete=models.CASCADE, null=True)
    sigmax = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    sigmay = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    sigmaz = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    geom = PointField(srid=28992)
    omschrijving = models.CharField(max_length=256, blank=True, null=True)
    z = models.FloatField(null=True)
    # picture = models.ImageField(upload_to="meetbouten_pictures/",
    #                             blank=True, null=True)
    #
    # def picture_tag(self):
    #     return mark_safe(f'<img src="{settings.MEDIA_URL}{self.picture}" width="50" height="50" />')
    # picture_tag.short_description = 'Picture'


class Meting(models.Model):
    class Meta:
        verbose_name_plural = "Metingen"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    inwindatum = models.DateField()
    wijze_inwinning = models.ForeignKey(WijzenInwinning, on_delete=models.CASCADE, null=True)
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    hoogte = models.FloatField()
    metingtype = models.ForeignKey(Metingtype, on_delete=models.CASCADE, db_column="mty_id")


class MetingHerzien(models.Model):
    class Meta:
        verbose_name = "Meting herziening"
        verbose_name_plural = "Metingen herzieningen"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    inwindatum = models.DateField()
    wijze_inwinning = models.ForeignKey(WijzenInwinning, on_delete=models.CASCADE, null=True)
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    hoogte = models.FloatField()
    metingtype = models.ForeignKey(Metingtype, on_delete=models.CASCADE, db_column="mty_id")


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
        verbose_name_plural = "Controlepunten"

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
        verbose_name = "Meting referentiepunt"
        verbose_name_plural = "Metingen referentiepunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    meting = models.ForeignKey(Meting, on_delete=models.CASCADE, db_column="met_id")


class MetRefPuntenHerz(models.Model):
    class Meta:
        verbose_name = "Meting referentiepunt herziening"
        verbose_name_plural = "Metingen referentiepunten herzieningen"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    meting = models.ForeignKey(MetingHerzien, on_delete=models.CASCADE, db_column="met_id")


class Kringpunt(models.Model):
    class Meta:
        verbose_name_plural = "Kringpunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id")
    bouwblok = models.ForeignKey(Bouwblok, on_delete=models.CASCADE, db_column="bou_nummer")
    volgorde = models.IntegerField()

