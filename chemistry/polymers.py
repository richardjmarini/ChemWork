#!/usr/bin/env python3

from .registery import RegisterSubClasses
from .parser import Parser

class Polymer(Parser, metaclass= RegisterSubClasses):

    def __init__(self, *args, **kwargs):

        super(Polymer, self).__init__()

        self.id= id(self)

        self.get_elements()

    def __str__(self):

        label= getattr(self, 'name')
        if label is None:
            label= getattr(self, 'symbol')
            if label is None:
                label= getattr(self, 'smiles')
               
        return '%s (id= %s)' % (label, self.id)

