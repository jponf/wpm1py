# -*- coding: utf-8 -*-

#
#
class SATSolver:
    """
    Abstract layer between WPM1 algorithm and the underlying sat solver
    """

    def solve(self, num_vars, formula):
        """
        solve(num_vars:int, formula:[]/set): bool, core/truth_assigantion

        Takes the input formula and number of variables and use a SAT solver
        to solve it, then return the result in an specific format

        Input:
            - num_vars: Number of the 

            - formula: Could be any iterable data structure filled with clauses

        Output:
            A tuple (bool, set/[])

            The first component indicates if the formula is satisfiable(True) or
            unsatisfiable(False).

            The second component depens on the first one:
                True: Truth assignation that satisfies the formula as an iterable
                False: Core clauses as an iterable of iterables
        """
        raise NotImplementedError('solve( num_vars, formula ). Abstract method')