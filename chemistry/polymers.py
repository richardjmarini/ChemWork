#!/usr/bin/env python3

from uuid import uuid4
from networkx import draw, spring_layout
import matplotlib.pyplot as plt

from .registery import RegisterSubClasses
from .parser import Parser

class Polymer(Parser, metaclass= RegisterSubClasses):

    def __init__(self, *args, **kwargs):

        super(Polymer, self).__init__()

        self.id= uuid4() # id(self)

        self.get_elements()

    def __str__(self):

        label= getattr(self, 'name')
        if label is None:
            label= getattr(self, 'symbol')
            if label is None:
                label= getattr(self, 'smiles')
               
        return '%s (id= %s)' % (label, self.id)


def show(polymer):

    draw(
        polymer.transformer.graph,
        with_labels= True,
        font_size= 8
    )
    plt.show()
