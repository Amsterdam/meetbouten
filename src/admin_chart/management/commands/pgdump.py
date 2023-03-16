import os
import logging

from subprocess import Popen

from django.core.files.storage import get_storage_class
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    file_name = "meetbouten.dump"

    def handle(self, *args, **options):
        database = settings.DATABASES['default']
        success = self.start_dump(database)
        if success:
            self.upload_to_blob()
            self.remove_dump()

    def start_dump(self, database: dict):
        command = f'pg_dump --host={database["HOST"]} ' \
            f'--dbname={database["NAME"]} ' \
            f'--username={database["USER"]} ' \
            f'--no-password ' \
            f'--file={self.file_name}'
        try:
            proc = Popen(command, shell=True, env={
                'PGPASSWORD': database['PASSWORD']
            })
            proc.wait()
            logger.info("dumping of the db was succesfull")
            return True
        except Exception as e:
            logger.critical('Unable to pg_dump the database')
            logger.exception(e)
            return False

    def upload_to_blob(self) -> str:
        storage = get_storage_class()()
        with open(self.file_name, "rb") as f:
            storage.save(name=f"pg_dump/{self.file_name}", content=f)
        logger.info("PG dump uploaded to storage")

    def remove_dump(self):
        """
        Removes the files locally when processing is done
        """
        os.remove(self.file_name)
