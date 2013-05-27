# -*- coding: utf-8 -*-

import MSatFormula

#TODO check algorithm

class WPM1:

	#
	#
	def __init__(self, formula, sat_solver):
		self.formula = formula
		self.sat_solver = sat_solver

	#
	#
	def solve():
		"""
		solve(): (cost:int, assignation/core: [])

		Tries to solve the formula using the WPM1 algorithm

		Returns
			cost: integer value which represents the cost of solving the given
					formula or negative if the formula is unsatisfiable

			assignation/core: A list filled with the truth values assignation if
					the formula is satisfiable or the core if it is unsatisfiable
		"""

		sat, core = self._checkHardClauses()
		if not sat:
			return (-1, core)

		cost = 0
		wmax = self.formula.maxWeightLessThan( MSatFormula.INFINITY )

		while True:
			sformula = self.formula.getFormula(wmax)
			sat, sout = self.sat_solver.solve(sformula)

			if wmax == 0 and sat:
				return (cost, sout)
			elif sat:
				wmax = self.formula.maxWeightLessThan(wmax)
			else:
				blocking_vars = []
				wmin = self.formula.minWeightOfClauses(sout)

				for c in sout:
					if not self.formula.isHardClause(c):
						b = self.formula.relaxClause(c, wmin)
						blocking_vars.append(b)

				self.formula.addCardinalityConstraint(blocking_vars,
													MSatFormula.EXACTLY_ONE, 
													MSatFormula.INFINITY )
				cost += wmin
	#
	#
	def _checkHardClauses():
		"""
		Handles the hard clauses satisfiability comprovation
		"""
		hard_formula = self.formula.getHardClausesFormula()
		return self.sat_solver.solve(hard_formula)
