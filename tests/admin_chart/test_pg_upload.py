import os

from django.conf import settings
from django.core.management import call_command

from admin_chart.management.commands.pgdump import Command

FILEPATH = Command.file_path


class TestPgdumpCommand:
    def test_pg_dump_create_file(self):
        database = settings.DATABASES["default"]
        Command().start_dump(database)
        assert os.path.isfile(FILEPATH)
        os.remove(FILEPATH)

    def test_pg_dump_upload(self):
        f = open(FILEPATH, "w")
        f.close()
        Command().upload_to_blob()
        assert os.path.isfile(FILEPATH)
        os.remove(FILEPATH)

    def test_pg_dump_remove(self):
        f = open(FILEPATH, "w")
        f.close()
        Command().remove_dump()
        assert not os.path.isfile(FILEPATH)

    def test_pg_dump(self):
        """
        Check the whole happy flow
        """
        call_command("pgdump")
        assert not os.path.isfile(FILEPATH)  # No file left after upload
