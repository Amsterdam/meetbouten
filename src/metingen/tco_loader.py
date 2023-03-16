import re
from typing import NamedTuple

from tablib import Dataset
from import_export.formats.base_formats import TablibFormat

from io import StringIO


class MetingTCO(NamedTuple):
    hoogtepunt: str
    x: float
    y: float
    hoogte: float
    header: str


class TCOFormatClass(TablibFormat):
    def get_title(self):
        return "tco"

    def get_extension(self):
        "extension for export-file"
        return "tco"

    def create_dataset(self, in_stream, **kwargs) -> Dataset():
        """
        Create tablib.dataset from .tco file
        """
        metingen = self.get_metingen(self._string_output(in_stream))
        data = [tuple(i) for i in metingen]

        return Dataset(*data, headers=MetingTCO._fields)

    def export_data(self, dataset, escape_output=False, **kwargs):
        """
        Create .tco with pre-defined-format from arg dataset
        """

        with StringIO() as tmp:

            _header = dataset["header"][0]
            for h in _header:
                tmp.write(h)
            tmp.write("$\n")

            spaces = [4, 15, 8, 13, 13, 13, 15]

            # data
            for meting in dataset:
                _row = ""
                for space, col in [
                    (4, 0),
                    (15, 1),
                    (8, 2),
                    (13, 3),
                    (13, 5),
                    (13, 6),
                    (13, 7),
                ]:
                    blank = " " * space
                    _row += blank + str(meting[col])
                _row += "\n"
                tmp.write(_row)
            tmp.write("$")

            dataset = tmp.getvalue()

        return dataset

    def get_metingen(self, stream) -> list[MetingTCO]:
        """
        Extract metingen from data
        """
        metingen = []
        _data = stream.split("$")
        _header = "$".join(_data[0:3])
        metingen_raw = _data[3].splitlines()
        for raw in metingen_raw:
            if raw:
                meting = self._interpret_meting(raw, _header)
                metingen.append(meting)

        return metingen

    @staticmethod
    def _interpret_meting(meting_raw, _header) -> MetingTCO:
        """
        Interpret meting from raw data
        """
        values = meting_raw.split()
        assert len(values) >= 4, "Each meting must have at least 4 values"
        hoogtepunt, x, y, z, *_ = values  # for tco less values than in cor
        z = re.sub("[^.0-9]", "", z)  # Remove all non-numeric characters
        meting = MetingTCO(hoogtepunt, x, y, hoogte=float(z), header=_header)
        return meting

    @staticmethod
    def _string_output(stream) -> str:
        """
        Accept either a str/bytes stream or a file-like object and always return a
        string object.
        """
        if isinstance(stream, bytes):
            return str(stream, "UTF-8")
        return stream
