# -*- coding: utf-8 -*-

#
#
class SATSolver:
    """Abstract layer between WPM1 algorithm and the underlying sat solver
    """

    def solve(self, num_vars, formula):
        """solve(num_vars:int, formula:[]/set): (bool, core/truth_assigantion)

        Takes as input a sat formula and the number of variables in the formula,
        then uses a SAT solver to solve it and returns the result in an specific
        format detailed below.

        Input:
            - num_vars: Number of variables in the formula (Can be greater)

            - formula: Can be any iterable data structure filled with clauses
                F.E: set([[1,2,-3],[-2,3,-5]])

        Output:
            A tuple (bool, set/[])

            The first component indicates if the formula is satisfiable(True) or
            unsatisfiable(False).

            The second component depends on the first one:
                True: Truth assignation that satisfies the formula as an iterable
                False: Core clauses as an iterable of iterables

                F.E:
                    - If True -> [1,-2,3]
                    - If False -> [[1,2], [-1,2], [1,-2], [-1,-2]]
        """
        raise NotImplementedError('solve( num_vars, formula ). Abstract method')
