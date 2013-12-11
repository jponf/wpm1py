# -*- coding: utf-8 -*-

import satsolver
import sys, os, errno, platform

#
#
class PicoSAT(satsolver.SATSolver):
    """Solves SAT formulas by using PicoSAT as the underlying sat solver
    """

    FORMULA_FILE_NAME = 'binutils/formula.picosat.cnf'
    OUTPUT_FILE_NAME = 'binutils/out.picosat.cnf'
    CORE_FILE_NAME = 'binutils/core.picosat.cnf'

    #
    #
    def __init__(self):
        """Initialize a new PicoSAT instance
        """
        self.__setSolverBinary()

    #
    #
    def solve(self, num_vars, formula):
        """solve(): (bool, []/set) // See solver.py
        """

        # Write formula to file and execute solver
        self.__writeFormula(num_vars, formula)
        os.system('%s -c %s %s > %s' % (self.solver_bin,
                                        PicoSAT.CORE_FILE_NAME,
                                        PicoSAT.FORMULA_FILE_NAME,
                                        PicoSAT.OUTPUT_FILE_NAME))

        sat = self.__checkSatisfiability()
        if sat:
            proof_or_core = self.__getProof()
        else:
            proof_or_core = self.__getCore()

        # Delete files to avoid possible problems due to unfinished operations
        # caused by: unhandled exceptions, etc
        self.__delTempFiles()

        return sat, proof_or_core

    #
    #   Write the given formula to a temp file
    def __writeFormula(self, num_vars, formula):
        """__writeFormula(num_vars, formula): void

            Writes the given formula to FORMULA_FILE_NAME.

            If there is any error then prints the information and raises the
            same error to the caller.
        """
        ff = None

        try:
            ff = open(PicoSAT.FORMULA_FILE_NAME, 'w')

            print >>ff, 'p cnf', num_vars, len(formula)

            for clause in formula:
                for lit in clause:
                    print >>ff, lit,
                print >>ff, '0'

        except IOError as e:
            sys.stderr.write(
                "[PicoSAT] __writeFormula(...): I/O Error({0}) {1}\n".format(
                                                        e.errno, e.strerror))
            raise e

        finally:
            if ff:
                ff.close()

    #
    #   Check if solver output contains the s SATISFIABLE message
    def __checkSatisfiability(self):

        try:

            f = open(PicoSAT.OUTPUT_FILE_NAME, 'r')
            for l in f:
                if 's SATISFIABLE' == l.strip():
                    return True

            return False

        except IOError as e:
            sys.stderr.write(
                "[PicoSAT] __checkSatisfiability(): I/O Error({0}) {1}\n"
                                .format(e.errno, e.strerror) )
            raise e
        finally:
            f.close()

    #
    #   Returns a set with all the literals of the satisfiability proof
    def __getProof(self):

        proof = set()

        try:
            f = open(PicoSAT.OUTPUT_FILE_NAME, 'r')

            for l in f:
                if l[0] == 'v':
                    dummy, sapace, values = l.partition(' ')
                    for val in map( int, values.split(' ') ):
                        if val != 0:
                            proof.add( int(val) )

        except IOError as e:
            sys.stderr.write(
                "[PicoSAT] __getProof(): I/O Error({0}) {1}\n".format(
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
            f = open(PicoSAT.CORE_FILE_NAME, 'r')

            for l in f:
                try:
                    values = map(int, l.split())
                    del values[-1]
                    core.add(frozenset(values))

                except ValueError:
                    pass

        except IOError as e:
            sys.stderr.write(
                "[PicoSAT] __getCore(): I/O Error({0}) {1}\n".format(
                                                        e.errno, e.strerror))
            raise e
        finally:
            f.close()

        return core

    #
    #   Delete temporal files
    def __delTempFiles(self):
        try:
            os.remove(PicoSAT.FORMULA_FILE_NAME)
            os.remove(PicoSAT.OUTPUT_FILE_NAME)
            os.remove(PicoSAT.CORE_FILE_NAME)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise e

    #
    #   Set the solver binary based on the platform and the architecture
    def __setSolverBinary(self):
        system = platform.system()
        architecture = platform.architecture()[0]

        if system == 'Linux':
            if architecture == '64bit':
                self.solver_bin = 'binutils/picosat_linux_x64'
            else:
                self.solver_bin = 'binutils/picosat_linux_x86'  # TODO: Test it on a x86 machine :D
        elif system == 'Darwin':
            if architecture == '64bit':
                self.solver_bin = 'binutils/picosat_osx_intel64'
            else:
                raise EnvironmentError('There is no binary file for Darwin i386')
        else:
            raise EnvironmentError('There is no binary file for %s' %
                                    (system) )

        # Check if is executable
        if os.path.isfile(self.solver_bin):
            if not os.access(self.solver_bin, os.X_OK):
                raise EnvironmentError('%s is not marked as executable' %
                                    (self.solver_bin) )
        else:
            raise EnvironmentError('Missing binary file "%s"' %
                                                            (self.solver_bin) )


#
#
if __name__ == '__main__':

    formula_unsat = [[1,2],[-1,2],[1,-2], [-1, -2]]
    formula_sat = [[1,2], [-1,2], [1,-2]]
    p = PicoSAT()

    print p.solve(2, formula)
