# -*- coding: utf-8 -*-

import msatformula

#
#
class Formula(msatformula.MSatFormula):

    #
    #
    def getHardClausesFormula( self):
        super(Formula, self).getHardClausesFormula()

    #
    #
    def getFormulaWithMinWeight( self, min_weight ):
        super(Formula, self).getFormulaWithMinWeight( min_weight )

    #
    #
    def maxWeightLessThan( self, upper_bound ):
        super(Formula, self).maxWeightLessThan(upper_bound)

    #
    #
    def minWeightOfClauses( self, clauses ):

        wmin = self.inf
        clause = None

        for clause in clauses:
            try:
                cw = self.clauses_weights[clause]
                if cw < wmin:
                    wmin = cw
            except:
                raise LookupError('Clause %s is not in the formula' % str(clause))

        return wmin

    #
    #
    def relaxClause( self, clause, weight ):
        super(Formula, self).relaxClause(clause, weight)

    #
    #
    def addCardinalityConstraint( self, literals, cctype, weight ):
        super(Formula, self).addCardinalityConstraint(literals, cctype, weight)

    #
    #
    def isHardClause( self, clause ):
        super(Formula, self).isHardClause(clause)
