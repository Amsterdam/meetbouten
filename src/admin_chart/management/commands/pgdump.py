import csv
import logging
import os
from datetime import datetime
from subprocess import Popen
import django.apps
import psycopg2
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.management.base import BaseCommand

from django.db import connection
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    TMP_DIRECTORY = "/tmp/pg_dump"

    def handle(self, *args, **options):
        folder_name = timezone.now().strftime("%Y-%m-%d")  # folder name is current date
        tmp_dir = os.path.join(self.TMP_DIRECTORY, folder_name)
        self.start_dump(tmp_dir)
        self.upload_to_blob(tmp_dir, folder_name)
        self.remove_dump(tmp_dir)
        logger.info("Completed DB dump")


    def start_dump(self, tmp_dir: str):
        os.makedirs(tmp_dir, exist_ok=True)
        # give everybody read/write access to the directory
        app_names = settings.LOCAL_APPS
        for app in app_names:
            # get models from app name
            for model in django.apps.apps.get_app_config(app).get_models():
                qs = model.objects.all()
                filepath = os.path.join(tmp_dir, f"{model.__name__}.csv")  # filename is model name
                self._dump_model_to_csv(filepath, qs)

    def _dump_model_to_csv(self, filepath, qs):
        fieldnames = [field.name for field in qs.model._meta.fields]
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)  # write queryset header
            for obj in qs:
                writer.writerow([getattr(obj, name) for name in fieldnames])
        logger.info(f"Successfully dumped {filepath}")

    def upload_to_blob(self, tmp_dir: str, folder_name: str):
        storage = get_storage_class()()
        for file in os.listdir(tmp_dir):
            filepath = os.path.join(tmp_dir, file)
            with open(filepath, "rb") as f:
                storage.save(name=os.path.join(folder_name, file), content=f)
            logger.info(f"Successfully uploaded {filepath} to blob")

    def remove_dump(self, tmp_dir: str):
        """
        Removes the files locally when processing is done
        """
        for file in os.listdir(tmp_dir):
            filepath = os.path.join(tmp_dir, file)
            os.remove(filepath)