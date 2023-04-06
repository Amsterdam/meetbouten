from django.contrib.gis.db.models import PointField
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.safestring import mark_safe

from main import settings
from metingen.hoogtepunt_nummer_generator import HoogtepuntNummerGenerator
from referentie_tabellen.models import (
    Bron,
    Merk,
    Metingtype,
    Status,
    Type,
    WijzenInwinning,
)

GENERATOR = HoogtepuntNummerGenerator()
GENERATOR.load_bladnummers()


class Hoogtepunt(models.Model):
    class Meta:
        verbose_name_plural = "Hoogtepunten"

    class Windrichtingen(models.TextChoices):
        N = "N", "Noord"
        NO = "NO", "Noord-Oost"
        NW = "NW", "Noord-West"
        O = "O", "Oost"
        W = "W", "West"
        Z = "Z", "Zuid"
        ZO = "ZO", "Zuid-Oost"
        ZW = "ZW", "Zuid-West"

    id = models.AutoField(primary_key=True)
    nummer = models.CharField(
        max_length=8, blank=True, validators=[MinLengthValidator(8)]
    )
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column="typ_nummer")
    agi_nummer = models.CharField(
        max_length=8, null=True, blank=True
    )  # Rijkswaterstaat nummer
    vervaldatum = models.DateField(null=True, blank=True)
    omschrijving = models.CharField(max_length=256, blank=True, null=True)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE, db_column="mer_id")
    xmuur = models.FloatField(blank=True, null=True)
    ymuur = models.FloatField(blank=True, null=True)
    windr = models.CharField(
        max_length=2, null=True, blank=True, choices=Windrichtingen.choices
    )
    sigmax = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    sigmay = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    geom = PointField(srid=28992, blank=True)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, db_column="sta_id", null=True, blank=True
    )
    orde = models.IntegerField(null=True, blank=True)
    picture = models.ImageField(upload_to="meetbouten_pictures/", blank=True, null=True)

    def __str__(self):
        return f"{self.nummer} - {self.type.omschrijving}"

    def save(self, *args, **kwargs):
        if not self.nummer:
            self.nummer = GENERATOR.generate(self)
        super().save(*args, **kwargs)

    def picture_tag(self):
        if self.picture:
            return mark_safe(
                f'<img src="{settings.MEDIA_URL}{self.picture}" width="50" height="50" />'
            )

    picture_tag.short_description = "Picture"


class Grondslagpunt(models.Model):
    class Meta:
        verbose_name_plural = "Grondslagpunten"

    id = models.AutoField(primary_key=True)
    nummer = models.CharField(max_length=8)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column="typ_nummer")
    rdnummer = models.DecimalField(
        max_digits=8, decimal_places=0, null=True, blank=True
    )
    orde = models.DecimalField(max_digits=1, decimal_places=0)
    inwindatum = models.DateField()
    vervaldatum = models.DateField(null=True, blank=True)
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    wijze_inwinning = models.ForeignKey(
        WijzenInwinning,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="wijze_inwinning",
    )
    sigmax = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    sigmay = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    sigmaz = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    geom = PointField(srid=28992)
    omschrijving = models.CharField(max_length=256, blank=True, null=True)
    z = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.nummer} - {self.type.omschrijving}"


class Meting(models.Model):
    class Meta:
        verbose_name = "Meting [Archief tm 2009]"
        verbose_name_plural = "Metingen [Archief tm 2009]"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    inwindatum = models.DateField()
    wijze_inwinning = models.ForeignKey(
        WijzenInwinning,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="wijze_inwinning",
    )
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    hoogte = models.DecimalField(max_digits=6, decimal_places=4)
    metingtype = models.ForeignKey(
        Metingtype, on_delete=models.CASCADE, db_column="mty_id"
    )

    def __str__(self):
        return f"{self.metingtype} - {self.hoogtepunt.nummer}"


class MetingHerzien(models.Model):
    """In 2008 herziening NAP stelsel hoogtes. Bouten bleken toch te zakken. Amsterdam 15mm gezakt"""

    class Meta:
        verbose_name = "Meting"
        verbose_name_plural = "Metingen"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    inwindatum = models.DateField()
    wijze_inwinning = models.ForeignKey(
        WijzenInwinning,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="wijze_inwinning",
    )
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    hoogte = models.DecimalField(max_digits=6, decimal_places=4)
    metingtype = models.ForeignKey(
        Metingtype, on_delete=models.CASCADE, db_column="mty_id"
    )

    def __str__(self):
        return f"{self.metingtype} - {self.hoogtepunt.nummer}"


class MetingReferentiepunt(models.Model):
    class Meta:
        verbose_name = "Referentiepunt [Archief tm 2009]"
        verbose_name_plural = "Referentiepunten [Archief tm 2009]"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    meting = models.ForeignKey(Meting, on_delete=models.CASCADE, db_column="met_id")


class MetRefPuntenHerz(models.Model):
    class Meta:
        verbose_name = "Referentiepunt"
        verbose_name_plural = "Referentiepunten"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    meting = models.ForeignKey(
        MetingHerzien, on_delete=models.CASCADE, db_column="met_id"
    )


class MetingControle(models.Model):
    class Meta:
        verbose_name = "Meting [ter controle]"
        verbose_name_plural = "Metingen [ter contole]"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    inwindatum = models.DateField()
    sigmaz = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    hoogte = models.DecimalField(max_digits=6, decimal_places=4)
    wijze_inwinning = models.ForeignKey(
        WijzenInwinning,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="wijze_inwinning",
    )
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, db_column="bro_id")
    metingtype = models.ForeignKey(
        Metingtype, on_delete=models.CASCADE, db_column="mty_id"
    )

    def __str__(self):
        return f"{self.hoogtepunt}"


class MetingVerrijking(models.Model):
    class Meta:
        verbose_name = "Meting [verrijking]"
        verbose_name_plural = "Metingen [verrijking]"

    id = models.AutoField(primary_key=True)
    hoogtepunt = models.ForeignKey(
        Hoogtepunt, on_delete=models.CASCADE, db_column="hoo_id"
    )
    x = models.DecimalField(max_digits=10, decimal_places=4)
    y = models.DecimalField(max_digits=10, decimal_places=4)
    hoogte = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    inwindatum = models.DateField(null=True, blank=True)
    c1 = models.DecimalField(max_digits=6, decimal_places=4, default=1.0000)
    c2 = models.DecimalField(max_digits=6, decimal_places=4, default=1.0000)
    c3 = models.DecimalField(max_digits=6, decimal_places=4, default=0.0000)
    header = models.CharField(max_length=60)
    file_name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.hoogtepunt}"
