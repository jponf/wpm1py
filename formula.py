#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msatformula
import sys

#
#
class Formula(msatformula.MSatFormula):

    #
    #
    def __init__( self, num_variables, inf, clauses ):
        """
        Initialize a new formula

        - num_variables: number of different variables in the formula

        - clauses: An iterable of tuples with the following format (weight, clause)
        """
        self.hard_clauses = set()
        self.soft_clauses = set()
        self.clauses_weights = {}
        self.inf = inf

        self.nvars = num_variables
        for w, c in clauses:
            self.__addClause(c, w)


    #
    # Override
    def getHardClausesFormula( self ):
        return (self.nvars, set(self.hard_clauses))

    #
    # Override
    def getFormulaWithMinWeight( self, min_weight ):
        if min_weight > self.inf:
            return []

        rf = set(self.hard_clauses)
        rf.update( [c for c in self.soft_clauses 
                        if self.clauses_weights[c] >= min_weight] )

        return (self.nvars, rf)


    #
    # Override
    def getMaxWeightLessThan( self, upper_bound ):
        if upper_bound <= 0:
            raise Exception('upper_bound can not be 0 or negative')

        # First dummy implementation
        w = 0

        for k, cw in self.clauses_weights.iteritems():
            if cw < upper_bound and cw > w:
                w = cw

        return w

    #
    # Override
    def getMinWeightOfClauses( self, clauses ):

        wmin = self.inf
        clause = None

        for clause in clauses:

            try:
                cw = self.clauses_weights[clause]
                if cw < wmin:
                    wmin = cw
            except:
                raise LookupError('Clause %s do not belong to the formula' % str(clause))

        return wmin

    #
    # Override
    def relaxClause( self, clause, weight ):

        if clause not in self.soft_clauses:
            raise LookupError('Clause %s do not belong to the formula' % str(clause))

        nvar = self.__newVariable()
        rclause = set(clause)
        rclause.add(nvar)

        self.clauses_weights[clause] -= weight
        self.clauses_weights[rclause] = weight
        self.soft_clauses.add(rclause)

        return nvar

    #
    # Override
    def addCardinalityConstraint( self, literals, cctype, weight ):

        if weight == msatformula.MSatFormula.INFINITY:
            weight = self.inf

        if cctype == msatformula.MSatFormula.EXACTLY_ONE:
            self.__addExcatlyOneConstraint(literals, weight)
        elif cctype == msatformula.MSatFormula.AT_MOST_ONE:
            self.__addAtMostOneConstraint(literals, weight)
        elif cctype == msatformula.MSatFormula.AT_LEAST_ONE:
            self.__addAtLeastOneConstraint(literals, weight)
        else:
            raise AttributeError('Unknown cctype value: %s' % str(cctype))


    #
    # Override
    def isHardClause( self, clause ):
        return clause in self.hard_clauses

    #
    #
    def __addClause( self, clause, weight):
        # Repeated clauses can have greater value than inf
        if type(clause) != frozenset:
            clause = frozenset(clause) # Dictionaries need it

        # If the clause is hard leave it as is
        if clause not in self.hard_clauses:
            # Restrict values to be at most inf
            w = min(self.clauses_weights.get(clause, 0) + weight, self.inf)

            if clause in self.soft_clauses:
                if w == self.inf:
                    self.hard_clauses.add(clause)
                    self.soft_clauses.remove(clause)
            else:
                if w == self.inf:
                    self.hard_clauses.add(clause)
                else:
                    self.soft_clauses.add(clause)

            self.clauses_weights[clause] = w

    #
    #
    def __addExcatlyOneConstraint(self, literals, weight):
        self.__addAtLeastOneConstraint(literals, weight)
        self.__addAtMostOneConstraint(literals, weight)

    #
    #
    def __addAtLeastOneConstraint(self, literals, weight):
        clause = frozenset(literals)
        self.__addClause( clause, weight )

    #
    #
    def __addAtMostOneConstraint(self, literals, weight):

        if type(literals) != list:
            literals = list(literals)
     

        for i in xrange( len(literals)-1 ):
            for j in xrange(i+1, len(literals) ):
                clause = frozenset( (-literals[i], -literals[j]) )  
                self.__addClause(clause, weight)

    #
    #
    def __newVariable(self):
        self.nvars += 1
        return self.nvars   