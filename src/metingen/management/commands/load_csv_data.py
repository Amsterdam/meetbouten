import logging

from django.core.management.base import BaseCommand
from django.db import connection

from metingen.models import *
from bouwblokken.models import *

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
        "nullable_fields": ["VERVALDATUM", "WINDR"]
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
        "nullable_fields": ["VERVALDATUM"]
    },
    {
        "model": MetingHerzien,
        "file": "GRS_metingen_herz.csv",
        "fields": ["ID", "HOO_ID", "INWINDATUM", "WIJZE_INWINNING", "SIGMAZ", "BRO_ID", "HOOGTE", "MTY_ID"],
    },
    {
        "model": Meting,
        "file": "GRS_metingen.csv",
        "fields": ["ID", "HOO_ID", "INWINDATUM", "WIJZE_INWINNING", "SIGMAZ", "BRO_ID", "HOOGTE", "MTY_ID"],
    },
    {"model": Bouwblok, "file": "GRS_bouwblokken.csv", "fields": ["NUMMER", "AANSLUITPNT", "CONTROLEPNT", "OPMERKING"]},
    {"model": Controlepunt, "file": "GRS_controlepunten.csv", "fields": ["BOU_NUMMER", "HOO_ID"]},
    {"model": Referentiepunt, "file": "GRS_referentiepunten.csv", "fields": ["BOU_NUMMER", "HOO_ID"]},
    {"model": MetingReferentiepunt, "file": "GRS_metingenreferentiepunten.csv", "fields": ["MET_ID", "HOO_ID"]},
    {"model": MetRefPuntenHerz, "file": "GRS_met_ref_punten_herz.csv", "fields": ["MET_ID", "HOO_ID"]},
    {"model": Kringpunt, "file": "GRS_kringpunten.csv", "fields": ["BOU_NUMMER", "VOLGORDE", "HOO_ID"]},
]


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--num-bb',
    #         type=int,
    #         help='The number of BB permits to create',
    #     )

    def handle(self, *args, **options):
        command_datestyle = 'ALTER DATABASE meetbouten SET datestyle TO "ISO, DMY";'
        with connection.cursor() as cursor:
            cursor.execute(command_datestyle)

        for dump in data_config:
            table_name = dump["model"]._meta.db_table
            force_null = f", FORCE_NULL({','.join(dump['nullable_fields'])})" if "nullable_fields" in dump else ""
            command = (
                f"COPY {table_name}({','.join(dump['fields'])}) "
                f"FROM '/csv_dump/{dump['file']}' "
                f"WITH (FORMAT CSV, DELIMITER ',', HEADER {force_null});"
            )
            print(command)
            with connection.cursor() as cursor:
                cursor.execute(command)
