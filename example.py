#!/usr/bin/env python

from chemistry import Adenine

from chemistry.elements import Element
from chemistry.polymers import Polymer, show
from chemistry.bonds import Bond

print('Available', Element)
print('Available', Polymer)
print('Available', Bond)

a= Adenine()
print(a)
show(a)
