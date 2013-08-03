# -*- coding: utf-8 -*-

from msatformula import MSatFormula

#TODO check algorithm

class WPM1:

    #
    #
    def __init__(self, formula, sat_solver):
        self.formula = formula
        self.sat_solver = sat_solver

    #
    #
    def solve(self):
        """
        solve(): (cost:int, assignation/core: [])

        Solves the formula using the WPM1 algorithm

        Returns
            cost: integer value which represents the cost of solving the given
                    formula or negative if the formula is unsatisfiable

            assignation/core: A list filled with the truth values assignation if
                    the formula is satisfiable or the core if it is unsatisfiable
        """
        nvars, formula = self.formula.getHardClausesFormula()
        sat, core = self.sat_solver.solve(nvars, formula)
        if not sat: return (-1, core)

        cost = 0
        wmax = self.formula.getMaxWeightLessThan( MSatFormula.INFINITY )

        while True:
            nvars, formula = self.formula.getFormulaWithMinWeight(wmax)
            sat, sout = self.sat_solver.solve(nvars, formula)

            if wmax == 0 and sat:
                return (cost, sout)
            elif sat:
                wmax = self.formula.getMaxWeightLessThan(wmax)
            else:
                blocking_vars = []
                wmin = self.formula.getMinWeightOfClauses(sout)

                for c in sout:
                    
                    if not self.formula.isHardClause(c):
                        b = self.formula.relaxClause(c, wmin)
                        blocking_vars.append(b)
   
                self.formula.addCardinalityConstraint(blocking_vars,
                                                    MSatFormula.EXACTLY_ONE, 
                                                    MSatFormula.INFINITY )
                cost += wmin