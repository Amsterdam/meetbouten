import string

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from metingen.models import Hoogtepunt
from .models import (
    Bouwblok,
    Referentiepunt,
    Controlepunt,
    Kringpunt,
)


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
