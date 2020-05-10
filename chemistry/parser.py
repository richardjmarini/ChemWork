#!/usr/bin/env python3

from lark import Lark
from lark.exceptions import ParseError
from glob import glob
from os import getcwd
from os.path import basename, splitext

from .smiles import Smiles

class Parser(object):

    def __init__(self):

        super(Parser, self).__init__()

        self.parser= None
        self.input_stream= None
        self.setup()

    def setup(self):

        cwd= getcwd()
        for filename in glob('%s/**/*.lark' % (cwd), recursive=True):

            (fmt, ext)= splitext(basename(filename))
            if fmt in self.__class__.__dict__.keys():
                self.input_stream= getattr(self.__class__, fmt)
                grammer= open(filename, 'r').read()
                transformer= Smiles()
            else:
                continue

            self.parser= Lark(
                grammer,
                parser= "lalr",
                debug= False,
                transformer= transformer
            )

    def get_elements(self):

        print('\nINPUT STREAM:', self.input_stream, '\n')

        try:
            tree= self.parser.parse(self.input_stream)
        except Exception as e:
           print('ERROR',str(e), e.__class__.__dict__)
           raise

        print('\n')
        for blah in tree.children:
            print('>>>', blah)

