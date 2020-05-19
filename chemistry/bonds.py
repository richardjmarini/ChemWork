#!/usr/bin/env python3

from uuid import uuid4
from .registery import RegisterSubClasses

class Bond(object, metaclass= RegisterSubClasses):

    def __init__(self, elements, number_of_electrons):

        super(Bond, self).__init__()

        self.id= uuid4() #id(self)
        self.elements= elements
        self.number_of_electrons= number_of_electrons

    def __str__(self):

        label= getattr(self, 'name')

        return '%s (id= %s, number_of_electrons= %s)' % (label, self.id, self.number_of_electrons)

