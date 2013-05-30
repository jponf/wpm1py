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
        self.weights = set()
        self.clauses_weights = {}
        self.inf = inf

        self.nvars = num_variables
        for w, c in clauses:
            self.__addClause(c, w)


    #
    #
    def getHardClausesFormula( self ):
        return (self.nvars, set(self.hard_clauses))

    #
    #
    def getFormulaWithMinWeight( self, min_weight ):
        if min_weight > self.inf:
            return []

        rf = list(self.hard_clauses)
        rf.extend( [c for c in self.soft_clauses 
                        if self.clauses_weights[c] >= min_weight] )

        return (self.nvars, rf)


    #
    #
    def maxWeightLessThan( self, upper_bound ):
        if upper_bound <= 0:
            raise Exception('upper_bound can not be 0 or negative')

        # First dummy implementation
        w = 0

        for cw in self.weights:
            if cw < upper_bound and cw > w:
                w = cw

        return w

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
                raise LookupError('Clause %s do not belong to the formula' % str(clause))

        return wmin

    #
    #
    def relaxClause( self, clause, weight ):

        if type(clause) != frozenset:
            clause = frozenset(clause)

        if clause not in self.soft_clauses:
            raise LookupError('Clause %s do not belong to the formula' % str(clause))

        nvar = self.__newVariable()
        rclause = set(clause)
        rclause.add(nvar)

        self.clauses_weights[clause] -= weight
        self.clauses_weights[rclause] = weight
        self.soft_clauses.add(rclause)
        self.weights.add(weight)

        return nvar

    #
    #
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
    #
    def isHardClause( self, clause ):
        return clause in self.hard_clauses

    #
    #
    def __addClause( self, clause, weight):

        if type(clause) != frozenset:
            clause = frozenset(clause) # Dictionaries need it

        if weight >= self.inf:
            self.hard_clauses.add(clause)
        else:
            self.soft_clauses.add(clause)

        self.__setClauseWeight( clause, weight )

    #
    #
    def __setClauseWeight( self, clause, weight):

        if weight > self.inf:
            weight = self.inf
            sys.stderr.write('WARNING: Clause with weight above infinity: '
                             '%s' % str(clause) )

        self.weights.add(weight)
        if self.clauses_weights.has_key(clause):
            self.clauses_weights[clause] += weight
        else:
            self.clauses_weights[clause] = weight

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