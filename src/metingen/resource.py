import re

import tablib
from import_export.formats.base_formats import TextFormat
from import_export.resources import ModelResource

from metingen.models import MetingControle, Hoogtepunt


class CORFormat(TextFormat):
    TABLIB_MODULE = "tablib.formats._csv"
    CONTENT_TYPE = "text/csv"

    def create_dataset(self, in_stream, **kwargs):
        if isinstance(in_stream, bytes) and self.encoding:
            in_stream = in_stream.decode(self.encoding)

        new_stream = self.reformat_cor_to_csv(in_stream)
        return tablib.import_set(new_stream, format=self.get_title())

    def reformat_cor_to_csv(self, in_stream):
        dollar_signs = 0
        new_stream = "hoogtepunt,hoogte,sigmaz\n"
        for row in in_stream.splitlines():
            if row == "$":
                dollar_signs += 1
                continue
            if dollar_signs == 3 and row:
                meting = self._interpret_meting(meting_raw=row)
                new_stream += ",".join(meting) + "\n"
        return new_stream

    def _interpret_meting(self, meting_raw) -> tuple:
        # Interpret meting from raw data
        values = meting_raw.split()
        assert len(values) >= 4, "Each meting must have at least 4 values"
        puntnummer, x, y, z, *_, sigmaz = values
        z = re.sub("[^.0-9]", "", z)  # Remove all non-numeric characters
        meting = [puntnummer, z, sigmaz]
        return meting


class MetingControleResource(ModelResource):
    class Meta:
        model = MetingControle
        exclude = ["id"]
        import_id_fields = ["hoogtepunt"]

    def before_import_row(self, row, row_number=None, **kwargs):
        row["hoogtepunt"] = Hoogtepunt.objects.get(nummer=row["hoogtepunt"]).id
        row["inwindatum"] = kwargs.get("inwindatum")
        row["bron"] = kwargs.get("bron").id
        row["wijze_inwinning"] = kwargs.get("wijze_inwinning").id
        row["metingtype"] = kwargs.get("metingtype").id
