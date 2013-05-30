# -*- coding: utf-8 -*-


#
#
class Solver:
    """
    Abstract layer between WPM1 algorithm and the sat solver
    """

    def solve(self, num_vars, formula):
        """
        solve(num_vars:int, formula:[clauses]): bool, core/truth_assigantion

        Takes the input formula and number of variables and use a SAT solver
        to solve it, then return the result in an specific format

        Input:
            - formula: Could be any iterable data structure filled with clauses

        Output:
            A tuple (bool, [])

            The first component indicates if the formula is satisfiable(True) or
            unsatisfiable(False).

            The second component depens on the first one:
                True: Truth assignation that satisfies the formula
                False: Core clauses
        """
