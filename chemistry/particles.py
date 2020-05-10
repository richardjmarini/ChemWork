#!/usr/bin/env python3

from .registery import RegisterSubClasses

class Particle(object, metaclass= RegisterSubClasses):
     pass

class Electron(Particle):
    pass

class Proton(Particle):
    pass

class Neutron(Particle):
    pass
