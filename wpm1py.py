#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import signal
import sys

import wpm1formula
import wcnfparser
import satsolver
import wpm1


__program__ = 'WPM1PY'
__author__ = 'Josep Pon Farreny <jpf2@alumnes.udl.cat>'
__version__ = '0.5'
__licence__ = 'GPL'
__status__ = "Stable"


def main():
    global options

    registerSignals()

    try:
        parser = wcnfparser.WCNFParser(options.infile)
        solver = loadSolver(options.solver)

        num_vars, top, clauses = parser.parse()
        if options.infile != sys.stdin:
            options.infile.close()
        formula = wpm1formula.Formula(num_vars, top, clauses)

        algorithm = wpm1.WPM1(formula, solver)
        cost, proof = algorithm.solve()

        if cost == wpm1.WPM1.WPM1_UNKNOWN:
            printUnknown(proof)
        else:
            printResult(cost, proof)

    except MemoryError as e:
        printUnknown('Out of memory')

    except Exception as e:
        sys.stderr.write('{0}: {1}\n'.format(e.__class__.__name__, str(e)))
        # Uncoment the name below to get the stack trace
        #raise


def printResult(cost, proof, lits_per_line=30):

    if cost >= 0:
        print 'o', cost
        print 's OPTIMUM FOUND'

        print 'v',
        for ind, lit in enumerate(sorted(proof, key=abs), 1):
            print lit,
            if ind % lits_per_line == 0:
                print '\nv',
        print

    else:

        print 's UNSATISFIABLE'
        print 'c Core Clauses'

        for clause in proof:
            print 'c',
            for lit in clause:
                print lit,
            print '0'


def printUnknown(reason):

    print 's UNKNOWN'

    if reason:
        for line in reason.split('\n'):
            print 'c %s' % line


def loadSolver(solver):

    components = solver.split('.')

    first_module = components[0]
    components = components[1:]

    try:
        mod = __import__(first_module)
    except ImportError:
        raise ImportError(
            'Error importing the solver module: %s' % first_module)

    try:
        for comp in components:
            mod = getattr(mod, comp)
    except AttributeError:
        raise ImportError(
            'Error importing the solver "%s". The attribute "%s" does not exist'
            % (solver, comp))

    if issubclass(mod, satsolver.SATSolver):
        return mod()
    else:
        raise ImportError(
            'Error the specified solver class %s '
            'does not inherit satsolver.SATSolver' % solver)


def registerSignals():
    signal.signal(signal.SIGXCPU, signal_handler)


def signal_handler(signal, frame):

    if signal == signal.SIGXCPU:
        printUnknown("CPU usage exceeded")

# Program entry point, calls immediatly the main routine
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Educational implementation of WPM1')

    parser.add_argument(
        'infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help='Path to a cnf/wcnf file. If not specified it will be stdin')

    parser.add_argument(
        '-s', '--solver', action='store', default='solvers.picosat.PicoSAT',
        help='Solver wrapper used to perform underlying SAT operations. '
             'Default: solvers.picosat.PicoSAT')

    options = parser.parse_args()

    main()
