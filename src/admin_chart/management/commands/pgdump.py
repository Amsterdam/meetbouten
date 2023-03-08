import logging
from subprocess import PIPE, Popen
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    file_name = "pgdump.dat"

    def handle(self, *args, **options):
        database = settings.DATABASES['default']
        success = self.start_dump(database)
        if success:
            self.upload_to_blob()

    def start_dump(self, database: dict):
        command = f'pg_dump --host={database["HOST"]} ' \
            f'--dbname={database["NAME"]} ' \
            f'--username={database["USER"]} ' \
            f'--no-password ' \
            f'--file=meetbouten.dump '
        try:
            proc = Popen(command, shell=True, env={
                'PGPASSWORD': database['PASSWORD']
            })
            proc.wait()
            return True
        except Exception as e:
            logger.critical('Unable to pg_dump the database')
            logger.exception(e)
            return False

    def upload_to_blob(self):
        pass
        ##TODO:: Implement the upload to Azure feature to make it possible to upload the file to azure.

