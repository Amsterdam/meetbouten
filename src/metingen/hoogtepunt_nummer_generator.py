import csv
from typing import NamedTuple


class Kaartblad(NamedTuple):
    bladnr: str
    xmin: int
    xmax: int
    ymin: int
    ymax: int


class HoogtepuntNummerGenerator:
    def __init__(self):
        self.bladnummers = []

    def load_bladnummers(
        self, filename: str = "/src/metingen/files/kaartbladen.csv"
    ) -> list[Kaartblad]:
        if len(self.bladnummers) > 0:
            return self.bladnummers
        with open(filename, "r") as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
                values = {
                    k: str(v) if k == "bladnr" else int(v) for k, v in row.items()
                }
                self.bladnummers.append(Kaartblad(**values))
        return self.bladnummers

    def generate(self, hoogtepunt) -> str:
        x, y = hoogtepunt.geom.tuple
        nummer = self.get_bladnr(x=x, y=y)
        nummer += "8"
        nummer += self.get_bouttype_nr(bouttype_nr=hoogtepunt.type.nummer)
        nummer += self.get_volgnr(nummer)
        return nummer

    def get_bladnr(self, x: int, y: int) -> str:
        for blad in self.bladnummers:
            if blad.xmin <= x < blad.xmax and blad.ymin <= y < blad.ymax:
                return blad.bladnr
        return "000"

    def get_bouttype_nr(self, bouttype_nr: int) -> str:
        bouttype_mapping = {6: 0, 7: 1, 8: 9, 9: 8}
        return str(bouttype_mapping[bouttype_nr])

    def get_volgnr(self, nummer):
        from metingen.models import Hoogtepunt

        hoogtepunten = Hoogtepunt.objects.filter(nummer__startswith=nummer)
        volgnrs = [int(h.nummer[-3:]) for h in hoogtepunten]
        max_nr = max(volgnrs) if len(volgnrs) > 0 else 0
        return str(max_nr + 1).zfill(3)
