import logging

from django.core.management.base import BaseCommand

from bouwblokken.factories import (
    BouwblokFactory,
    ControlepuntFactory,
    KringpuntFactory,
    ReferentiepuntFactory,
)
from bouwblokken.models import Bouwblok, Controlepunt, Kringpunt, Referentiepunt
from metingen.factories import (
    GrondslagpuntFactory,
    HoogtepuntFactory,
    MetingFactory,
    MetingHerzFactory,
    MetingReferentiepuntFactory,
    MetRefPuntenHerzFactory,
)
from metingen.models import (
    Grondslagpunt,
    Hoogtepunt,
    Meting,
    MetingHerzien,
    MetingReferentiepunt,
    MetRefPuntenHerz,
)

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--num",
            type=int,
            help="The number of records to create of every kind",
        )

    def handle(self, *args, **options):
        num = options.get("num", 1000)
        self.create_data(num)

    def create_data(self, num):
        factories_list = [
            (HoogtepuntFactory, Hoogtepunt),
            (GrondslagpuntFactory, Grondslagpunt),
            (MetingFactory, Meting),
            (MetingHerzFactory, MetingHerzien),
            (MetingReferentiepuntFactory, MetingReferentiepunt),
            (MetRefPuntenHerzFactory, MetRefPuntenHerz),
            (BouwblokFactory, Bouwblok),
            (ControlepuntFactory, Controlepunt),
            (ReferentiepuntFactory, Referentiepunt),
            (KringpuntFactory, Kringpunt),
        ]
        for factory, model in factories_list:
            factory_data = factory.build_batch(size=num)
            model.objects.bulk_create(factory_data)

        log.info(f"Created data")
