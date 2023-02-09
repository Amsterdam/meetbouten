import logging

from django.core.management.base import BaseCommand

from meetbouten.factories import (
    GrondslagpuntFactory,
    MetingReferentiepuntFactory,
    MetRefPuntenHerzFactory,
    ControlepuntFactory,
    ReferentiepuntFactory,
    KringpuntFactory, MetingFactory, HoogtepuntFactory, MetingHerzFactory, BouwblokFactory,
)
from meetbouten.models import Grondslagpunt, MetingReferentiepunt, MetRefPuntenHerz, Controlepunt, Referentiepunt, \
    Kringpunt, Meting, Hoogtepunt, MetingHerzien, Bouwblok

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
            [r.save() for r in factory_data]
            # model.objects.bulk_create(factory_data)

        log.info(f"Created data")
