#!/usr/bin/env python3

from networkx import MultiGraph, path_graph
from lark import Transformer, v_args, Token, Tree
from logging import getLogger

import chemistry

class Smiles(Transformer):

    ELECTRON_MAP= {
        '-': 1,
        '=': 2,
        '#': 3,
        '$': 4,
        ':': 5,
        '/': 6,
        '\\': 7,
        '.': 8
    }

    def __init__(self):

        super(Smiles, self).__init__()

        self.previous_element= None
        self.current_bond= None
        self.ring_number= None
        self.rings= {}

        # should this be a seperate meta class that various
        # parsers can use? 
        self.graph= MultiGraph()

    @v_args(inline= True)
    def atom(self, token):

        # create element we found 
        token.value= getattr(chemistry, token.value)()
        self.graph.add_node(token.value)
        print('created element:', token.value)

        if self.ring_number is not None:
            if self.ring_number in self.rings:
                # if there was a saved ring number [from the ring() method below]
                # and if this is the last element in an existing ring 
                # then bond the element to the element at the start of the ring
    
                elements=  [self.rings.get(self.ring_number), token.value]

                # TODO: determine number of electrons to use (defaulting to single for now)
                bond= getattr(chemistry, 'Covalent')(elements= elements, number_of_electrons= Smiles.ELECTRON_MAP['-'])
                for element in elements:
                    element.bonds.append(bond)

                # TODO: how do we we double and triple bonds?
                self.graph.add_edges_from([elements, ])

                print('creating ring bond %s with elements: %s\n' % (self.ring_number, list(map(str, elements))))
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

           # TODO: how do we we double and triple bonds?
            self.graph.add_edges_from([self.current_bond.elements,])

            print('bonding elements: %s with Bond(id= %s, number_of_electrons= %s)' % (list(map(str, self.current_bond.elements)), self.current_bond.id, self.current_bond.number_of_electrons))
            self.current_bond= None

        # clear the current ring number and set the previous element
        self.ring_number= None
        self.previous_element= token.value

        # when two atoms are back to back consider that a single bond
        # if we've gotten here then there is no current bond so setup a single bond
        # for the next atom() call
        self.current_bond= getattr(chemistry, 'Covalent')(elements= [token.value], number_of_electrons= Smiles.ELECTRON_MAP['-'])

        return token

    @v_args(inline= True)
    def bond(self, token):

        # if this is a bond then save the previous element to the bond
        elements= [self.previous_element]
        self.previous_element= None
        
        # create partial bond with the previous element 
        # seond element will be added to bond in above atom() emethod
        token.value= getattr(chemistry, 'Covalent')(elements= elements, number_of_electrons= Smiles.ELECTRON_MAP.get(token.value, 1))
        self.current_bond= token.value

        return token

    def branch(self, tokens):

       print('BRANCED FROM PREVIOUS', self.previous_element)
       print('FOUND branch:', tokens)
       print('FROM PREVIOUS ELEMENT', self.previous_element)
       for token in tokens[1:-1]:
           if type(token) == Token:
               print('\t>', token.value)
           elif type(token) == Tree:
               for _token in token.children:
                   if type(_token) == Token:
                       print('\t\t>', _token.value)
                   elif type(_token) == Tree:
                       for __token in _token.children:
                           print('\t\t\t<', __token.value)
 
       return token

    def RING(self, token):
    
        # if we found a ring then save it
        # this is used in the atom() method above
        self.ring_number= int(token.value)

        return token

