import re
from typing import NamedTuple

from metingen.models import MetingControle, Hoogtepunt


class Meting(NamedTuple):
    puntnummer: str
    x: float
    y: float
    z: float


class CORLoader:
    def __init__(self, path):
        self.path = path
        self.data = None

    def load(self):
        # Extract data from text file and load into Metingen controle model
        self.get_data()
        metingen = self.get_metingen()
        self.load_metingen_into_db(metingen)

    def get_data(self):
        # Extract data from text file
        with open(self.path, 'r') as f:
            self.data = f.read()

    def get_metingen(self) -> list[Meting]:
        # Extract metingen from data
        metingen = []
        data = self.data.split("$")[3]
        metingen_raw = data.splitlines()
        for raw in metingen_raw:
            if raw:
                meting = self._interpret_meting(raw)
                metingen.append(meting)
        return metingen

    def _interpret_meting(self, meting_raw) -> Meting:
        # Interpret meting from raw data
        values = meting_raw.split()
        assert len(values) >= 4, "Each meting must have at least 4 values"
        puntnummer, x, y, z, *_ = values
        z = re.sub("[^.0-9]", "", z)  # Remove all non-numeric characters
        meting = Meting(puntnummer, x=float(x), y=float(y), z=float(z))
        return meting

    def load_metingen_into_db(self, metingen):
        # Load metingen into Metingen controle model
        records = []
        for m in metingen:
            hoogtepunt = Hoogtepunt.objects.get(nummer=m.puntnummer)
            meting_record = MetingControle(hoogtepunt=hoogtepunt, x=m.x, y=m.y, hoogte=m.z)
            records.append(meting_record)
        MetingControle.objects.bulk_create(records)
