from collections import namedtuple

WijzeInwinning = namedtuple("WijzeInwinning", ["id", "omschrijving"])
wijzen_inwinning = [
    WijzeInwinning(1, "Waterpassing"),
    WijzeInwinning(2, "Tachymetrisch"),
    WijzeInwinning(3, "GPS"),
]

Type = namedtuple("Type", ["nummer", "omschrijving", "soort"])
types = [
    Type("1", "X,Y,(Z) Rijksdriehoeksmeting", "1"),
    Type("2", "X,Y,(Z) Hoofdnet GVI", "2"),
    Type("3", "X,Y,(Z) Verdichtng GVI", "5"),
    Type("6", "NAP-bout", "8"),
    Type("7", "Deformatiebout", "8"),
    Type("8", "Referentiebout", "8"),
    Type("9", "Ondergronds merk", "8"),
]

Status = namedtuple("Status", ["id", "omschrijving"])
statussen = [
    Status(1, "Actueel"),
    Status(2, "Niet te meten"),
    Status(3, "Vervallen"),
]

Metingtype = namedtuple("Metingtype", ["id", "omschrijving"])
metingtypen = [
    Metingtype(1, "Deformatiemeting"),
    Metingtype(2, "NAP-meting"),
]

Bron = namedtuple("Bron", ["id", "omschrijving", "doel"])
bronnen = [
    Bron(0, "Onbekend", "O"),
    Bron(1, "Onbekend", "O"),
    Bron(2, "GVI", "A"),
    Bron(3, "Fugro", "H"),
    Bron(4, "Lankelma", "H"),
    Bron(5, "Meetdienst", "H"),
    Bron(6, "RD", "G"),
    Bron(7, "RD kernnet", "G"),
    Bron(8, "MIU", "H"),
]

Merk = namedtuple("Merk", ["id", "omschrijving_verkort", "omschrijving"])
merken = [
    Merk(
        "18",
        "Koperen bout met opschrift XXX",
        "Ronde koperen bout met Amsterdamse kruizen ( 3 Andreas kruizen)",
    ),
    Merk("0", "Ronde bout met opschrift NAP", "Ronde bout met opschrift NAP"),
    Merk(
        "1",
        "Ronde bout",
        "Ronde bout of althans aan de bovenzijde ronde bout zonder opschrift of met opschrift anders dan NAP",
    ),
    Merk("2", "Kleine ronde bout", "Kleine ronde bout"),
    Merk("3", "Knopbout", "Knopbout"),
    Merk("4", "Vierkante bout", "Vierkante bout met of zonder groeven"),
    Merk("5", "Kleine ronde kruisbout", "Kleine ronde kruisbout"),
    Merk(
        "6",
        "Pijpbout",
        "Pijpbout met of zonder daarvoor geplaatste bronzen beschermingsplaat, hoogtepunt is midden gat",
    ),
    Merk(
        "7",
        "Bijzondere merktekens",
        "Bijzondere merktekens bijvoorbeeld zeskantige bout, stalen pen etc.",
    ),
    Merk(
        "+",
        "Grote kruisbout",
        "Grote kruisbout, vierkant bronzen kop met groeven, hoogtepunt is midden groef",
    ),
    Merk("13", "Kopbout", "Kopbout"),
    Merk(
        "14",
        "Inbusbout",
        "Inbusbout (cilinderschroef met binnenzeskant) in slaganker M6",
    ),
    Merk("16", "Koperen bout", "Koperen bout"),
    Merk("-", "Peilsteen", "Peilsteen"),
    Merk("20", "Aankoppelpunt waterleiding", "Aankoppelpunt waterleiding"),
    Merk("99", "Onbekend", "Onbekend"),
    Merk(
        "10",
        "Verticaal koperen boutje",
        "Verticaal koperen boutje, meestal in kunstwerk",
    ),
    Merk(
        "11",
        "Bovenkant stift in bout",
        "Bovenkant stift in vastleggingsbout, afhankelijk van hor. of vert. ",
    ),
    Merk("12", "Sondeerstaaf", "Sondeerstaaf"),
    Merk("15", "Koperen hakkelbout", "Koperen hakkelbout"),
    Merk("17", "RVS-bout", "Veelal gebruikt door 'de waal'"),
]
