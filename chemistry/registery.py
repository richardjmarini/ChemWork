#!/usr/bin/env python3

class RegisterSubClasses(type):

    def __init__(cls, name, bases, nmspc):

        super(RegisterSubClasses, cls).__init__(name, bases, nmspc)

        if not hasattr(cls, 'registry'):
            cls.registry = set()

        cls.registry.add(cls)
        cls.registry -= set(bases) 

    def __iter__(cls):

        return iter(cls.registry)

    def __str__(cls):

        if cls in cls.registry:
            return cls.__name__

        return cls.__name__ + ": " + ", ".join([sc.__name__ for sc in cls])
