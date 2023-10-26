import os
import shutil
from unittest.mock import patch

import pytest
from django.conf import settings
from django.core.management import call_command

from admin_chart.management.commands.pgdump import Command
from referentie_tabellen.models import Type
from referentie_tabellen.referentie_waardes import types


class TestPgdumpCommand:
    @patch("admin_chart.management.commands.pgdump.Command._dump_model_to_csv")
    def test_start_dump(self, mock_dump):
        tmp_dir = os.path.join(Command.TMP_DIRECTORY, "1980-01-01", "test.csv")
        Command().start_dump(tmp_dir)

        assert os.path.isdir(tmp_dir)
        assert mock_dump.called

    @pytest.mark.django_db
    def test_dump_model_csv(self):
        qs = Type.objects.all()
        filepath = os.path.join("/tmp", "test.csv")
        Command()._dump_model_to_csv(filepath, qs)
        assert os.path.isfile(filepath)
        # check if file contains header and 10 rows
        with open(filepath, "r") as f:
            assert len(f.readlines()) == 1 + len(types)
        os.remove(filepath)

    def test_upload_to_blob(self):
        folder_name = "01-01-1980"
        file_name = "test.csv"
        tmp_dir = os.path.join("/tmp", folder_name)
        os.makedirs(tmp_dir)
        open(os.path.join(tmp_dir, file_name), "w").close()
        assert os.path.isfile(os.path.join(tmp_dir, file_name))

        Command().upload_to_blob(tmp_dir, folder_name)
        stored_file = os.path.join(settings.MEDIA_ROOT, folder_name, file_name)
        assert os.path.isfile(stored_file)
        os.remove(stored_file)

    @pytest.mark.django_db
    def test_pg_dump(self):
        """
        Check the whole happy flow
        """

        def cleanup(path):
            tmp_folders = os.listdir(path)
            for folder in tmp_folders:
                shutil.rmtree(os.path.join(path, folder))

        call_command("pgdump")
        assert not os.listdir(Command.TMP_DIRECTORY)

        folder = os.listdir(settings.MEDIA_ROOT)[0]
        assert len(os.listdir(os.path.join(settings.MEDIA_ROOT, folder))) > 1

        cleanup(settings.MEDIA_ROOT)  # post cleanup
