import logging

from django.core.management.base import BaseCommand

from metingen.factories import MetingControleFactory
from metingen.models import MetingControle

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
            (MetingControleFactory, MetingControle),
        ]
        for factory, model in factories_list:
            factory_data = factory.build_batch(size=num)
            model.objects.bulk_create(factory_data)

        log.info(f"Created data")
