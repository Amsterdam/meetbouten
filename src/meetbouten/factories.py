# 3rd party
import string
import datetime

import factory
from django.utils import timezone
from factory import fuzzy
from factory.django import DjangoModelFactory

from constanten.models import Bron, Type, Metingtype, Status, Merk, WijzenInwinning
from .models import (
    Hoogtepunt,
    Grondslagpunt,
    Bouwblok,
    Meting,
    MetingHerzien,
    MetingReferentiepunt,
    MetRefPuntenHerz,
    Referentiepunt,
    Controlepunt,
    Kringpunt,
)


class HoogtepuntFactory(DjangoModelFactory):
    class Meta:
        model = Hoogtepunt

    nummer = fuzzy.FuzzyText(length=8, chars=string.digits)
    type = factory.Iterator(Type.objects.all())
    agi_nummer = fuzzy.FuzzyText(length=8)
    vervaldatum = fuzzy.FuzzyDate(start_date=timezone.now().date())
    omschrijving = factory.Faker("address")
    merk = factory.Iterator(Merk.objects.all())
    xmuur = fuzzy.FuzzyDecimal(low=-100, high=100)
    ymuur = fuzzy.FuzzyDecimal(low=-100, high=100)
    windr = fuzzy.FuzzyChoice(choices=["Z", "NW", "W", "N", "0", "NO", "ZW", "ZO", "O"])
    sigmax = 1
    sigmay = 1
    geom = "POINT (119411.7 487201.6)"
    status = factory.Iterator(Status.objects.all())
    orde = fuzzy.FuzzyInteger(low=0, high=1)


class GrondslagpuntFactory(DjangoModelFactory):
    class Meta:
        model = Grondslagpunt

    nummer = fuzzy.FuzzyText(length=8, chars=string.digits)
    type = factory.Iterator(Type.objects.all())
    rdnummer = fuzzy.FuzzyDecimal(low=25000000, high=26000000)
    orde = fuzzy.FuzzyInteger(low=1, high=3)
    inwindatum = fuzzy.FuzzyDate(start_date=datetime.date(year=1950, month=1, day=1), end_date=timezone.now().date())
    vervaldatum = fuzzy.FuzzyDate(start_date=timezone.now().date())
    bron = factory.Iterator(Bron.objects.all())
    wijze_inwinning = factory.Iterator(WijzenInwinning.objects.all())
    sigmax = fuzzy.FuzzyChoice(choices=[0, 1, 0.01, 0.02])
    sigmay = fuzzy.FuzzyChoice(choices=[0, 1, 0.01, 0.02])
    sigmaz = None
    geom = "POINT (119411.7 487201.6)"
    omschrijving = factory.Faker("address")
    z = fuzzy.FuzzyDecimal(low=-100, high=100)


class MetingFactory(DjangoModelFactory):
    class Meta:
        model = Meting

    hoogtepunt = factory.Iterator(Hoogtepunt.objects.all())
    inwindatum = fuzzy.FuzzyDate(start_date=datetime.date(year=1950, month=1, day=1), end_date=timezone.now().date())
    wijze_inwinning = factory.Iterator(WijzenInwinning.objects.all())
    sigmaz = fuzzy.FuzzyDecimal(low=0, high=0.01, precision=4)
    bron = factory.Iterator(Bron.objects.all())
    hoogte = fuzzy.FuzzyDecimal(low=-5, high=15, precision=4)
    metingtype = factory.Iterator(Metingtype.objects.all())


class MetingHerzFactory(MetingFactory):
    class Meta:
        model = MetingHerzien


class MetingReferentiepuntFactory(DjangoModelFactory):
    class Meta:
        model = MetingReferentiepunt

    hoogtepunt = factory.Iterator(Hoogtepunt.objects.all())
    meting = factory.Iterator(Meting.objects.all())


class MetRefPuntenHerzFactory(DjangoModelFactory):
    class Meta:
        model = MetRefPuntenHerz

    hoogtepunt = factory.Iterator(Hoogtepunt.objects.all())
    meting = factory.Iterator(MetingHerzien.objects.all())


class BouwblokFactory(DjangoModelFactory):
    class Meta:
        model = Bouwblok

    nummer = fuzzy.FuzzyText(length=4, prefix="MB", chars=string.digits)
    opmerking = fuzzy.FuzzyText(length=50)
    aansluitpunt = factory.Iterator(Hoogtepunt.objects.all())
    controlepunt = factory.Iterator(Hoogtepunt.objects.all())


class ControlepuntFactory(DjangoModelFactory):
    class Meta:
        model = Controlepunt

    hoogtepunt = factory.Iterator(Hoogtepunt.objects.all())
    bouwblok = factory.Iterator(Bouwblok.objects.all())


class ReferentiepuntFactory(DjangoModelFactory):
    class Meta:
        model = Referentiepunt

    hoogtepunt = factory.Iterator(Hoogtepunt.objects.all())
    bouwblok = factory.Iterator(Bouwblok.objects.all())


class KringpuntFactory(DjangoModelFactory):
    class Meta:
        model = Kringpunt

    hoogtepunt = factory.Iterator(Hoogtepunt.objects.all())
    bouwblok = factory.Iterator(Bouwblok.objects.all())
    volgorde = fuzzy.FuzzyInteger(low=1, high=160)
