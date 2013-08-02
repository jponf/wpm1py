# -*- coding: utf-8 -*-

import solver
import sys, os, errno


#
#
class Picosat(solver.SATSolver):
    """
    Solves SAT formulas by using Picosat as the underlying sat solver
    """

    # Change this variables to use another picosat version
    #SOLVER_BIN = 'binutils/picosat_linux_x64'
    SOLVER_BIN = 'binutils/picosat_osx_intel64'   
    FORMULA_FILE_NAME = 'binutils/formula.picosat.cnf'
    OUTPUT_FILE_NAME = 'binutils/out.picosat.cnf'
    CORE_FILE_NAME = 'binutils/core.picosat.cnf'

    #
    #
    def solve(self, num_vars, formula):
        """
        solve(): (bool, []/set) // See solver.py
        """

        # Write formula to file and execute solver
        self.__writeFormula(num_vars, formula)
        os.system('%s -c %s %s > %s' % (Picosat.SOLVER_BIN, 
                                        Picosat.CORE_FILE_NAME,
                                        Picosat.FORMULA_FILE_NAME,
                                        Picosat.OUTPUT_FILE_NAME))

        sat = self.__checkSatisfiability()
        if sat:
            proof_or_core = self.__getProof()
        else:
            proof_or_core = self.__getCore()

        # Delete files to avoid possible problems due to unfinished operations
        # caused by: unhandled exceptions, etc
        

        return sat, proof_or_core
    
    #
    #   Write the given formula to a temp file 
    def __writeFormula(self, num_vars, formula):
        """
        __writeFormula(num_vars, formula): void

            Writes the given formula to FORMULA_FILE_NAME if there is an
            error prints information and raises the same error
        """

        try:
            ff = open(Picosat.FORMULA_FILE_NAME, 'w')

            print >>ff, 'p cnf', num_vars, len(formula)

            for clause in formula:
                for lit in clause:
                    print >>ff, lit,
                print >>ff, '0'

        except IOError as e:
            sys.stderr.write("__writeFormula(...): I/O Error({0}) {1}\n".format(
                                                        e.errno, e.strerror))
            raise e
        finally:
            ff.close()

    #
    #   Check if solver output contains the s SATISFIABLE message
    def __checkSatisfiability(self):
        """

        """
        try:

            f = open(Picosat.OUTPUT_FILE_NAME, 'r')
            for l in f:
                if 's SATISFIABLE' == l.strip():
                    return True
    
            return False

        except IOError as e:
            sys.stderr.write("__checkSatisfiability(): I/O Error({0}) {1}\n"\
                                .format(e.errno, e.strerror))
            raise e
        finally:
            f.close()

    #
    #   Returns a set with all the literals of the satisfiability proof
    def __getProof(self):

        proof = set()

        try:
            f = open(Picosat.OUTPUT_FILE_NAME, 'r')
    
            for l in f:
                if l[0] == 'v':
                    dummy, sapace, values = l.partition(' ')
                    for val in map( int, values.split(' ') ):
                        if val != 0:
                            proof.add( int(val) )

        except IOError as e:
            sys.stderr.write("__getProof(): I/O Error({0}) {1}\n".format(
                                                        e.errno, e.strerror))
            raise e
        finally:
            f.close()

        return proof

    #
    #   Returns the unsatisfiability proof
    def __getCore(self):

        core = set()

        try:
            f = open(Picosat.CORE_FILE_NAME, 'r')

            for l in f:
                try:
                    values = map(int, l.split())
                    del values[-1]
                    core.add(frozenset(values))

                except ValueError:
                    pass

        except IOError as e:
            sys.stderr.write("__getCore(): I/O Error({0}) {1}\n".format(
                                                        e.errno, e.strerror))
            raise e
        finally:
            f.close()

        return core

    #
    #   Delete temporal files
    def __delTempFiles(self):
        try:
            os.remove(Picosat.FORMULA_FILE_NAME)
            os.remove(Picosat.OUTPUT_FILE_NAME)
            os.remove(Picosat.CORE_FILE_NAME)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise e

#
#
if __name__ == '__main__':

    formula_unsat = [[1,2],[-1,2],[1,-2], [-1, -2]]
    formula_sat = [[1,2], [-1,2], [1,-2]]
    p = Picosat()

    print p.solve(2, formula)