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
        self.previous_element= None
        self.current_bond= None
        self.rings= {}

    @v_args(inline= True)
    def atom(self, token):

        # create element we found 
        token.value= getattr(chemistry, token.value)()
        print('created element:', token.value)

        if self.ring_number is not None and self.ring_number in self.rings:
           # if there was a saved ring number [from the ring() method below]
           # and if this is the last element in an existing ring 
           # then bond the element to the element at the start of the ring

           elements=  [token.value, self.rings.get(self.ring_number)]

           bond= getattr(chemistry, 'Covalent')(elements, 1)
           for element in elements:
               element.bonds.append(bond)

           print('creating ring bond %s with elements: %s' % (self.ring_number, [element, token.value]))
           del self.rings[self.ring_number]

        else:
           # if this is the first element in the ring
           # then save it until we terminate the ring

           self.rings[self.ring_number]= token.value        


        if self.current_bond is not None:

            # if this is the seocnd element invovled in the bond
            # then bond the two elements together
            # note: first element was added to bind in below bond() method

            self.current_bond.elements.append(token.value)

            for element in self.current_bond.elements:
                element.bonds.append(self.current_bond)

            print('bonding elements: ', self.current_bond.elements, 'with', self.current_bond.number_of_electrons, 'electrons')
            self.current_bond= None

        # clear the current ring number and set the previous element
        self.ring_number= None
        self.previous_element= token.value
        return token

    @v_args(inline= True)
    def bond(self, token):

        # if this is a bond then save the previous element to the bond
        elements= [self.previous_element]
        self.previous_element= None
        
        # create partial bond with the previous element 
        # seond element will be added to bond in above atom() emethod
        token.value= getattr(chemistry, 'Covalent')(elements, Smiles.ELECTRON_MAP.get(token.value, 1))
        self.current_bond= token.value

        return token

    def branch(self, tokens):

       print('FOUND branch:')
       for token in tokens:
           if type(token) == Token:
               print('\t', token.value)
           elif type(token) == Tree:
               for _token in token.children:
                   print('\t', _token)
 
       return token

    def RING(self, token):
    
        # if we found a ring then save it
        # this is used in the atom() method above
        self.ring_number= int(token.value)

        return token

