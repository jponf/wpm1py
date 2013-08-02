#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, argparse, traceback

import wpm1formula
import wcnfparser

from wpm1 import WPM1
from picosat import Picosat

__program__='WPM1PY'
__author__ = 'Josep Pon Farreny <jpf2@alumnes.udl.cat>'
__version__ = '0.1a'
__licence__ = 'GPL'


#
#
def main():
    parser = argparse.ArgumentParser(
                            description='Educational implementation of WPM1')

    parser.add_argument('-f', '--file', action='store', default="",
                    required=True, help='Path to a wcnf file')

    options = parser.parse_args()

    try:
        num_vars, inf, clauses = wcnfparser.parse(options.file)

        formula = wpm1formula.Formula(num_vars, inf, clauses)

        # Create algorithm and sat solver
        picosat = Picosat()
        wpm1 = WPM1(formula, picosat)

        cost, proof = wpm1.solve()
        print 'Final cost:', cost
        print 'Proof', proof

    except Exception as e:
        traceback.print_exc()
        sys.stderr.write( '{0}: {1}\n'.format(e.__class__.__name__, str(e)) )

# Program entry point, calls immediatly the main routine
if __name__ == '__main__':
    main()
