import os
import pytest

from django.core.management import call_command
from django.conf import settings

from admin_chart.management.commands.pgdump import Command


class TestPgdumpCommand:

    def test_pg_dump_create_file(self):
        database = settings.DATABASES['default']
        succesfull = Command().start_dump(database)
        assert succesfull
        assert os.path.isfile("meetbouten.dump")
        os.remove('meetbouten.dump')

    def test_pg_dump_upload(self):
        f = open('meetbouten.dump', 'w')
        f.close()
        name = Command().upload_to_blob()
        assert "pg_dump/meetbouten" in name
        os.remove('meetbouten.dump')

    def test_pg_dump_remove(self):
        f = open('meetbouten.dump',  'w')
        f.close()

        Command().remove_dump()
        assert not os.path.isfile('meetbouten.dump')
        assert not os.path.isfile('pg_dump/meetbouten_12345.dump')

    def test_pg_dump(self):
        """
        Check the whole happy flow
        """
        try:
            call_command('pgdump')
        except Exception as e:
            print(e)
            assert False

