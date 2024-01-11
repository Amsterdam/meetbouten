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
        Command().start_dump()
        assert os.path.isdir(Command.TMP_DIRECTORY)
        assert mock_dump.called

        shutil.rmtree(Command.TMP_DIRECTORY)

    @pytest.mark.django_db
    def test_dump_model_csv(self):
        os.makedirs(Command.TMP_DIRECTORY, exist_ok=True)
        filepath = Command()._dump_model_to_csv(Type)

        assert os.path.isfile(filepath)
        # check if file contains header and 10 rows
        with open(filepath, "r") as f:
            assert len(f.readlines()) == 1 + len(types)
        os.remove(filepath)

    def test_upload_to_blob(self):
        os.makedirs(Command.TMP_DIRECTORY, exist_ok=True)
        file_name = "test.csv"
        open(os.path.join(Command.TMP_DIRECTORY, file_name), "w").close()
        assert os.path.isfile(os.path.join(Command.TMP_DIRECTORY, file_name))

        Command().upload_to_blob()
        stored_file = os.path.join(settings.MEDIA_ROOT, 'pgdump', file_name)
        assert os.path.isfile(stored_file)
        os.remove(stored_file)

    @pytest.mark.django_db
    def test_pg_dump(self):
        """
        Check the whole happy flow
        """
        call_command("pgdump")

        assert not os.path.isdir(Command.TMP_DIRECTORY)
        assert len(os.listdir(os.path.join(settings.MEDIA_ROOT, 'pgdump'))) > 1
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'pgdump'))  # post cleanup
