import re
from typing import NamedTuple

from tablib import Dataset
from import_export.formats.base_formats import TablibFormat
from io import StringIO


class Meting(NamedTuple):
    hoogtepunt: str
    hoogte: float
    sigmaz: float


class CORFormatClass(TablibFormat):
    def get_title(self):
        return "cor"

    def create_dataset(self, in_stream, **kwargs):
        """
        Create tablib.dataset from .cor file
        """
        metingen = self.get_metingen(self._string_output(in_stream))
        data = [tuple(i) for i in metingen]

        return Dataset(*data, headers=Meting._fields)

    def get_metingen(self, stream) -> list[Meting]:
        """
        Extract metingen from data
        """
        metingen = []
        _data = stream.split("$")[3]
        metingen_raw = _data.splitlines()
        for raw in metingen_raw:
            if raw:
                meting = self._interpret_meting(raw)
                metingen.append(meting)
        return metingen

    @staticmethod
    def _interpret_meting(meting_raw) -> Meting:
        """
        Interpret meting from raw data
        """
        values = meting_raw.split()
        assert len(values) >= 4, "Each meting must have at least 4 values"
        hoogtepunt, x, y, z, *_, sigmaz = values
        z = re.sub("[^.0-9]", "", z)  # Remove all non-numeric characters
        meting = Meting(hoogtepunt, hoogte=float(z), sigmaz=float(sigmaz))
        return meting

    @staticmethod
    def _string_output(stream) -> str:
        """
        Accept either a str/bytes stream or a file-like object and always return a
        string object.
        """
        if isinstance(stream, bytes):
            return str(stream, 'UTF-8')
        return stream


