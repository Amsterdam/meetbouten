import csv
import logging
import os
import shutil

import django.apps
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.management.base import BaseCommand

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
            # get models from app name
            for model in django.apps.apps.get_app_config(app).get_models():
                qs = model.objects.all()
                filepath = os.path.join(
                    self.TMP_DIRECTORY, f"{model.__name__}.csv"
                )  # filename is model name
                self._dump_model_to_csv(filepath, qs)

    def _dump_model_to_csv(self, filepath, qs):
        fieldnames = [field.name for field in qs.model._meta.fields]
        with open(filepath, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)  # write queryset header
            for obj in qs:
                writer.writerow([getattr(obj, name) for name in fieldnames])
        logger.info(f"Successfully dumped {filepath}")

    def upload_to_blob(self):
        storage = OverwriteStorage()
        for file in os.listdir(self.TMP_DIRECTORY):
            filepath = os.path.join(self.TMP_DIRECTORY, file)
            with open(filepath, "rb") as f:
                storage.save(name=os.path.join('pgdump', file), content=f)
            logger.info(f"Successfully uploaded {filepath} to blob")

    def remove_dump(self):
        """
        Removes the files locally when processing is done
        """
        shutil.rmtree(self.TMP_DIRECTORY)


class OverwriteStorage(get_storage_class()):
    """ Overwrite existing files instead of using hash postfixes. """
    def _save(self, name, content):
        self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name
