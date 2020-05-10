from csv import DictReader

from .elements import Element
from .polymers import Polymer
from .bonds import Bond

def create_classes(_type, _filename):

    fh= open(_filename, "r")
    reader= DictReader(fh)
    for row in reader:

        # make available by name
        globals()[row.get('name')]= type(row.get('name'), (_type, ), row)

        # make available by symbol
        if 'symbol' in row.keys():
            globals()[row.get('symbol')]= globals()[row.get('name')]

        # make available by forumla
        if 'formula' in row.keys():
            globals()[row.get('formula')]= globals()[row.get('name')]

    fh.close()

create_classes(Element, "chemistry/elements.csv")
create_classes(Polymer, "chemistry/polymers.csv")
create_classes(Bond, "chemistry/bonds.csv")
