import logging

from django.core.management.base import BaseCommand
from django.db import connection
from opentelemetry import trace

from bouwblokken.models import *
from metingen.models import *

tracer = trace.get_tracer(__name__)

log = logging.getLogger(__name__)


data_config = [
    {
        "model": Hoogtepunt,
        "file": "GRS_hoogtepunten.csv",
        "fields": [
            "ID",
            "NUMMER",
            "TYP_NUMMER",
            "AGI_NUMMER",
            "VERVALDATUM",
            "OMSCHRIJVING",
            "MER_ID",
            "XMUUR",
            "YMUUR",
            "WINDR",
            "SIGMAX",
            "SIGMAY",
            "GEOM",
            "STA_ID",
            "ORDE",
        ],
        "nullable_fields": ["VERVALDATUM", "WINDR"],
    },
    {
        "model": Grondslagpunt,
        "file": "GRS_grondslagpunten.csv",
        "fields": [
            "ID",
            "NUMMER",
            "TYP_NUMMER",
            "RDNUMMER",
            "ORDE",
            "INWINDATUM",
            "VERVALDATUM",
            "BRO_ID",
            "WIJZE_INWINNING",
            "SIGMAX",
            "SIGMAY",
            "SIGMAZ",
            "GEOM",
            "OMSCHRIJVING",
            "Z",
        ],
        "nullable_fields": ["VERVALDATUM"],
    },
    {
        "model": MetingHerzien,
        "file": "GRS_metingen_herz.csv",
        "fields": [
            "ID",
            "HOO_ID",
            "INWINDATUM",
            "WIJZE_INWINNING",
            "SIGMAZ",
            "BRO_ID",
            "HOOGTE",
            "MTY_ID",
        ],
    },
    {
        "model": Meting,
        "file": "GRS_metingen.csv",
        "fields": [
            "ID",
            "HOO_ID",
            "INWINDATUM",
            "WIJZE_INWINNING",
            "SIGMAZ",
            "BRO_ID",
            "HOOGTE",
            "MTY_ID",
        ],
    },
    {
        "model": Bouwblok,
        "file": "GRS_bouwblokken.csv",
        "fields": ["NUMMER", "AANSLUITPNT", "CONTROLEPNT", "OPMERKING"],
    },
    {
        "model": Controlepunt,
        "file": "GRS_controlepunten.csv",
        "fields": ["BOU_NUMMER", "HOO_ID"],
    },
    {
        "model": Referentiepunt,
        "file": "GRS_referentiepunten.csv",
        "fields": ["BOU_NUMMER", "HOO_ID"],
    },
    {
        "model": MetingReferentiepunt,
        "file": "GRS_metingenreferentiepunten.csv",
        "fields": ["MET_ID", "HOO_ID"],
    },
    {
        "model": MetRefPuntenHerz,
        "file": "GRS_met_ref_punten_herz.csv",
        "fields": ["MET_ID", "HOO_ID"],
    },
    {
        "model": Kringpunt,
        "file": "GRS_kringpunten.csv",
        "fields": ["BOU_NUMMER", "VOLGORDE", "HOO_ID"],
    },
]


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        with tracer.start_as_current_span("Load CSV Data") as span:
            self._handle(*args, **options)

    def _handle(self, *args, **options):
        for dump in data_config:
            model = dump["model"]
            table_name = model._meta.db_table
            force_null = (
                f", FORCE_NULL({','.join(dump['nullable_fields'])})"
                if "nullable_fields" in dump
                else ""
            )
            command = (
                f"COPY {table_name}({','.join(dump['fields'])}) "
                f"FROM '/csv_dump/{dump['file']}' "
                f"WITH (FORMAT CSV, DELIMITER ',', HEADER {force_null});"
            )
            log.debug(command)
            with connection.cursor() as cursor:
                cursor.execute(command)

            if model in (Meting, MetingHerzien, Hoogtepunt, Grondslagpunt):
                self.set_id_sequence_value(table_name)

    def set_id_sequence_value(self, table_name):
        command = f"""SELECT setval('{table_name}_id_seq', (
                        select max(id) from {table_name}  where id <> '99999999'
                ), true);"""
        log.debug(command)
        with connection.cursor() as cursor:
            cursor.execute(command)
