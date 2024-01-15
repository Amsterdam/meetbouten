import logging
import os
import shutil

import django.apps
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.management.base import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    TMP_DIRECTORY = "/tmp/pg_dump"

    def handle(self, *args, **options):
        self.start_dump()
        self.upload_to_blob()
        self.remove_dump()
        logger.info("Completed DB dump")

    def start_dump(self):
        os.makedirs(self.TMP_DIRECTORY, exist_ok=True)
        app_names = settings.LOCAL_APPS
        for app in app_names:
            for model in django.apps.apps.get_app_config(app).get_models():
                self._dump_model_to_csv(model)

    def _dump_model_to_csv(self, model):
        table_name = model._meta.db_table
        filepath = os.path.join(
            self.TMP_DIRECTORY, f"{table_name}.csv"
        )  # filename is model name
        with open(filepath, "w") as f:
            sql = (
                f"COPY (SELECT * FROM {model._meta.db_table}) TO STDOUT WITH CSV HEADER"
            )
            with connection.cursor() as cursor:
                cursor.copy_expert(sql, f)

        logger.info(f"Successfully dumped {filepath}")
        return filepath

    def upload_to_blob(self):
        storage = OverwriteStorage()
        for file in os.listdir(self.TMP_DIRECTORY):
            filepath = os.path.join(self.TMP_DIRECTORY, file)
            with open(filepath, "rb") as f:
                storage.save(name=os.path.join("pgdump", file), content=f)
            logger.info(f"Successfully uploaded {filepath} to blob")

    def remove_dump(self):
        """
        Removes the files locally when processing is done
        """
        shutil.rmtree(self.TMP_DIRECTORY)


class OverwriteStorage(get_storage_class()):
    """Overwrite existing files instead of using hash postfixes."""

    def _save(self, name, content):
        self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name
