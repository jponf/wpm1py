# -*- coding: utf-8 -*-

from msatformula import MSatFormula
from satsolver import SATSolver


class WPM1:

    WPM1_UNSATISFIABLE = -1
    WPM1_UNKNOWN = -2

    #
    #
    def __init__(self, formula, sat_solver):
        self.formula = formula
        self.sat_solver = sat_solver

    #
    #
    def solve(self):
        """solve(): (cost:int, assignation/core: [])

        Solves the formula using the WPM1 algorithm

        Returns
            cost: positive integer value which represents the cost of solving
                  the given formula or a negative value, if the formula is
                  unsatisfiable or if the solver finishes due to a time or
                  memory limit.

            assignation/core: A list filled with the truth values assignation if
                   the formula is satisfiable, the core if it is unsatisfiable
                   or a string if the solver can not determine the solution due
                   a time or memory limit (the string should contain the reason)
        """
        nvars, formula = self.formula.getHardClausesFormula()
        sat, core = self.sat_solver.solve(nvars, formula)

        if sat == SATSolver.SOLVER_UNSATISFIABLE:
            return (WPM1.WPM1_UNSATISFIABLE, core)

        cost = 0
        wmax = self.formula.getMaxWeightLessThan(MSatFormula.TOP)

        while True:
            nvars, formula = self.formula.getFormulaWithMinWeight(wmax)
            sat, sout = self.sat_solver.solve(nvars, formula)

            if wmax == 0 and sat == SATSolver.SOLVER_SATISFIABLE:
                return (cost, sout)
            elif sat == SATSolver.SOLVER_SATISFIABLE:
                wmax = self.formula.getMaxWeightLessThan(wmax)
            elif sat == SATSolver.SOLVER_UNSATISFIABLE:
                blocking_vars = []
                wmin = self.formula.getMinWeightOfClauses(sout)

                for c in sout:
                    if not self.formula.isHardClause(c):
                        b = self.formula.relaxClause(c, wmin)
                        blocking_vars.append(b)

                self.formula.addCardinalityConstraint(blocking_vars,
                                                      MSatFormula.EXACTLY_ONE,
                                                      MSatFormula.TOP)
                cost += wmin

            elif sat == SATSolver.SOLVER_UNKNOWN:
                return (WPM1.WPM1_UNKNOWN,
                        'Underlaying solver unknown result\n'
                        'It can be due to memory or cpu time limits')
