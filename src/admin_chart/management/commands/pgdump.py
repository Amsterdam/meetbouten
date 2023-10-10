import logging
import os
from datetime import datetime
from subprocess import Popen

from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    FILENAME_PREFIX = "meetbouten-db"
    DIRECTORY = "/src/media/pg_dump"
    AZ_CONTAINER_NAME = 'public'

    def handle(self, *args, **options):
        database = settings.DATABASES["default"]
        filename = self._get_filename()
        filepath = f"{self.DIRECTORY}/{filename}.sql"
        blob_filepath = f"{self.AZ_CONTAINER_NAME}/{filename}.sql"
        self.start_dump(database, filepath)
        self.upload_to_blob(filepath, blob_filepath)
        self.remove_dump(filepath)

    def start_dump(self, database: dict, filepath: str):
        command = (
            f'pg_dump --host={database["HOST"]} '
            f'--dbname={database["NAME"]} '
            f'--username={database["USER"]} '
            f"--no-password "
            f"--file={filepath}"
        )
        proc = Popen(command, shell=True, env={"PGPASSWORD": str(database["PASSWORD"])})
        proc.wait()
        logger.info("dumping of the db was succesfull")

    def upload_to_blob(self, filepath: str, blob_filepath: str):
        storage = get_storage_class()()
        with open(filepath, "rb") as f:
            storage.save(name=blob_filepath, content=f)
        logger.info("PG dump uploaded to storage")

    def remove_dump(self, filepath: str):
        """
        Removes the files locally when processing is done
        """
        os.remove(filepath)

    def _get_filename(self):
        file_name = f"{self.FILENAME_PREFIX}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        return file_name
