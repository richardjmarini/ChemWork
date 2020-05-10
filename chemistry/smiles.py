#!/usr/bin/env python3

from networkx import Graph
from lark import Transformer, v_args, Token, Tree
from logging import getLogger

import chemistry

class Smiles(Transformer):

    ELECTRON_MAP= {
        '-': 1,
        '=': 2,
        '#': 3,
        '$': 3,
        ':': 4,
        '/': 5,
        '\\': 6,
        '.': 7
    }

    def __init__(self):

        super(Smiles, self).__init__()

        self.ring_number= None

    @v_args(inline= True)
    def atom(self, token):

        token.value= getattr(chemistry, token.value)()

        print('created element:', token.value)

        return token

    def BOND(self, token):

        # TODO: find elements to bond (possibly by predicate ?)
        elements= []

        # TODO: determine the type of bond between the two elements (eg, ionic, covalent, metalic)
        token.value= getattr(chemistry, 'Covalent')(elements, Smiles.ELECTRON_MAP.get(token.value, 1))

        print('created bond:', token.value)
       
        return token

    def branch(self, tokens):

       # TODO: do something with this... (possibly by predicate?)

       print('FOUND branch:')
       for token in tokens:
           if type(token) == Token:
               print('\t', token.value)
           elif type(token) == Tree:
               for _token in token.children:
                   print('\t', _token)
 
       return token

    def RING(self, token):
    
        # TODO: idenify start and end of ring and bond elements (possibly by predicate?)

        print('FOUND ring:', token.value)
        self.ring_number= int(token.value)

        return token

