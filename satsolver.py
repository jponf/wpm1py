# -*- coding: utf-8 -*-


class SATSolver:
    """Abstract layer between WPM1 algorithm and the underlying sat solver
    """

    SOLVER_SATISFIABLE = 1
    SOLVER_UNSATISFIABLE = 0
    SOLVER_UNKNOWN = -1

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

            The first component indicates if the formula is satisfiable,
            unsatisfiable or unknown if the solver can't find an answer due to
            memory or time limitations

            The second component depends on the first one:
                SOLVER_SATISFIABLE: Truth assignation that satisfies the formula
                                    as an iterable
                SOLVER_UNSATISFIABLE: Core clauses as an iterable of iterables
                SOLVER_UNKNOWN: None

                F.E:
                    - If SOLVER_SATISFIABLE -> [1,-2,3]
                    - If SOLVER_UNSATISFIABLE -> [1,2], [-1,2], [1,-2], [-1,-2]
                    - If SOLVER_UNKNOWN -> None
        """
        raise NotImplementedError('solve( num_vars, formula ). Abstract method')
