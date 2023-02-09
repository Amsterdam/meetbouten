from django.core.management import call_command


def test_load_csv_data():
    call_command('load_csv_data')
