#!/usr/bin/env python3

from uuid import uuid4

from .particles import Electron, Proton, Neutron
from .registery import RegisterSubClasses

class Element(object, metaclass= RegisterSubClasses):

    def __init__(self, *args, **kwargs):

       self.id= uuid4() # id(self)
       self.electrons= [Electron()] * int(self.atomic_number)
       self.protons= [Proton()] * int(self.atomic_number)
       self.neutrons= [Neutron()] * abs(int(self.atomic_number) - int(float(self.atomic_mass)))
  
       self.bonds= []

    def __str__(self):

        label= getattr(self, 'name')
        if label is None:
            label= getattr(self, 'symbol')

        return '%s (id= %s)' % (label, self.id)

    def __len__(self):
        return 10
