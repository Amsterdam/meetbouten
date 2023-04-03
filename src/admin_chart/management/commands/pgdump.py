import logging
import os
from subprocess import Popen

from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    file_name = "meetbouten.dump"
    file_path = f"/src/media/pg_dump/{file_name}"

    def handle(self, *args, **options):
        database = settings.DATABASES["default"]
        self.start_dump(database)
        self.upload_to_blob()
        self.remove_dump()

    def start_dump(self, database: dict):
        command = (
            f'pg_dump --host={database["HOST"]} '
            f'--dbname={database["NAME"]} '
            f'--username={database["USER"]} '
            f"--no-password "
            f"--file={self.file_path}"
        )
        proc = Popen(command, shell=True, env={"PGPASSWORD": database["PASSWORD"]})
        proc.wait()
        logger.info("dumping of the db was succesfull")

    def upload_to_blob(self):
        storage = get_storage_class()()
        with open(self.file_path, "rb") as f:
            storage.save(name=f"pg_dump/{self.file_name}", content=f)
        logger.info("PG dump uploaded to storage")

    def remove_dump(self):
        """
        Removes the files locally when processing is done
        """
        os.remove(self.file_path)
