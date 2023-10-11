import os

from django.conf import settings
from django.core.management import call_command

from admin_chart.management.commands.pgdump import Command

FILEPATH = f"{Command.DIRECTORY}/{Command.FILENAME_PREFIX}.sql"


class TestPgdumpCommand:
    def test_pg_dump_create_file(self):
        database = settings.DATABASES["default"]
        filename = "/tmp/pg_dump.sql"
        Command().start_dump(database, filename)
        assert os.path.isfile(filename)
        os.remove(filename)

    def test_pg_dump_remove(self):
        f = open(FILEPATH, "w")
        f.close()
        Command().remove_dump(FILEPATH)
        assert not os.path.isfile(FILEPATH)

    def test_pg_dump_upload(self):
        f = open(FILEPATH, "w")
        f.close()
        blob_filepath = f"{Command.FILENAME_PREFIX}.sql"
        Command().upload_to_blob(FILEPATH, blob_filepath)
        assert os.path.isfile(f"/src/media/{blob_filepath}")
        os.remove(f"/src/media/{blob_filepath}")
        os.remove(FILEPATH)

    def test_pg_dump(self):
        """
        Check the whole happy flow
        """
        call_command("pgdump")
        # Check if directory is empty
        assert not os.listdir(Command.DIRECTORY)
