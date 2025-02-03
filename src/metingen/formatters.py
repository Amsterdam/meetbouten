"""
Project specifiek gedefinieerde import_export formats voor het
- lezen van .cor en .tco files
- schrijven van .tco files
"""

import re
from io import StringIO
from typing import NamedTuple

from import_export.formats.base_formats import TablibFormat
from tablib import Dataset


class Meting(NamedTuple):
    hoogtepunt: str
    x: float
    y: float
    hoogte: float
    sigmaz: float


class BaseformatsClass:
    @staticmethod
    def _string_output(stream) -> str:
        """
        Accept either a str/bytes stream or a file-like object and always return a
        string object.
        """
        if isinstance(stream, bytes):
            return str(stream, "UTF-8")
        return stream

    def get_metingen(self, stream) -> list[Meting]:
        """
        Extract metingen from data
        """

        metingen = []
        _data = stream.split("$")

        header = "$".join(_data[0:3])
        metingen_raw = _data[3].splitlines()

        for raw in metingen_raw:
            if raw:
                meting = self._interpret_meting(raw, self.get_title())
                metingen.append(meting)

        return metingen, header

    @staticmethod
    def _interpret_meting(meting_raw, format) -> Meting:
        """
        Interpret meting from raw data
        """
        values = meting_raw.split()
        assert len(values) >= 4, "Each meting must have at least 4 values"

        def clean_z(z):
            # Remove all non-numeric characters
            return re.sub("[^-.0-9]", "", z)

        if format == "cor":
            hoogtepunt, x, y, z, *_, sigmaz = values
            return Meting(
                hoogtepunt,
                x=None,
                y=None,
                hoogte=float(clean_z(z)),
                sigmaz=float(sigmaz),
            )

        elif format == "tco":
            hoogtepunt, x, y, z, *_ = values
            return Meting(hoogtepunt, x, y, hoogte=float(clean_z(z)), sigmaz=None)
        else:
            ValueError("format is niet gespecificeerd")


class CORFormatClass(TablibFormat, BaseformatsClass):
    def get_title(self):
        return "cor"

    def create_dataset(self, in_stream, **kwargs):
        """
        Create tablib.dataset from .cor file
        """
        metingen, _ = self.get_metingen(self._string_output(in_stream))
        data = [tuple(i) for i in metingen]

        return Dataset(*data, headers=Meting._fields)


class TCOFormatClass(TablibFormat, BaseformatsClass):
    def get_title(self):
        return "tco"

    def get_extension(self):
        "extension for export-file"
        return "tco"

    def create_dataset(self, in_stream, **kwargs) -> Dataset():
        """
        Create tablib.dataset from .tco file
        """
        metingen, header = self.get_metingen(self._string_output(in_stream))
        data = [tuple(i) + (header,) for i in metingen]

        return Dataset(*data, headers=Meting._fields + ("header",))

    def export_data(self, dataset, escape_output=False, **kwargs):
        """
        Create .tco with pre-defined-format from arg dataset
        """
        with StringIO() as tmp:
            # write header
            _header = dataset["header"][0]
            for h in _header:
                tmp.write(h)
            tmp.write("$\n")

            # write data with specified spacing
            for meting in dataset:
                _row = ""
                for var in range(8):  # column "inwindatum" not in exportfile
                    mvar = str(meting[var])

                    # add blanks to string
                    if var == 0:
                        _mvar = mvar.rjust(12).ljust(19)
                    else:
                        _mvar = mvar.rjust(19)

                    _row += _mvar

                _row += "\n"
                tmp.write(_row)
            tmp.write("$")

            dataset = tmp.getvalue()

        return dataset
