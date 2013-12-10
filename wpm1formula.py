#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msatformula
import sys

#
#
class Formula(msatformula.MSatFormula):

    #
    #
    def __init__( self, num_variables, top, clauses ):
        """Initializes a new formula

        Parameters:
            - num_variables: number of different variables in the formula

            - clauses: An iterable of tuples with the following format
                       (weight, clause)
        """
        self.hard_clauses = set()
        self.soft_clauses = set()
        self.clauses_weights = {}
        self.top = top

        self.nvars = num_variables
        for w, c in clauses:
            self.__addClause(w, c)


    #
    # Override (See base class specification)
    def getHardClausesFormula( self ):
        return (self.nvars, self.hard_clauses)

    #
    # Override (See base class specification)
    def getFormulaWithMinWeight( self, min_weight ):
        if min_weight > self.top:
            return set()

        rf = set(self.hard_clauses)
        rf.update( [c for c in self.soft_clauses
                        if self.clauses_weights[c] >= min_weight] )

        return (self.nvars, rf)


    #
    # Override (See base class specification)
    def getMaxWeightLessThan( self, upper_bound ):
        if upper_bound == msatformula.MSatFormula.TOP:
            upper_bound = self.top

        if upper_bound <= 0:
            raise Exception('upper_bound can not be 0 or negative')

        # First dummy implementation
        w = 0

        for k, cw in self.clauses_weights.iteritems():
            if cw < upper_bound and cw > w:
                w = cw

        return w

    #
    # Override (See base class specification)
    def getMinWeightOfClauses( self, clauses ):

        wmin = self.top
        clause = None

        for clause in clauses:

            try:
                cw = self.clauses_weights[clause]
                if cw < wmin:
                    wmin = cw
            except:
                raise LookupError('Clause %s do not belong to the formula' %
                                                                    str(clause))

        return wmin

    #
    # Override (See base class specification)
    def relaxClause( self, clause, weight ):

        if clause not in self.soft_clauses:
            raise LookupError('Clause %s do not belong to the formula' %
                                                                    str(clause))

        nvar = self.__newVariable()
        rclause = set(clause)
        rclause.add(nvar)
        rclause = frozenset(rclause)

        self.clauses_weights[clause] -= weight
        self.clauses_weights[rclause] = weight
        self.soft_clauses.add(rclause)

        # Check if the previous clause now does not penalize when falsified
        # If so remove it
        if self.clauses_weights[clause] == 0:
            del self.clauses_weights[clause]
            self.soft_clauses.remove(clause)



        return nvar

    #
    # Override (See base class specification)
    def addCardinalityConstraint( self, literals, cctype, weight ):

        if weight == msatformula.MSatFormula.TOP:
            weight = self.top

        if cctype == msatformula.MSatFormula.EXACTLY_ONE:
            self.__addExcatlyOneConstraint(literals, weight)
        elif cctype == msatformula.MSatFormula.AT_MOST_ONE:
            self.__addAtMostOneConstraint(literals, weight)
        elif cctype == msatformula.MSatFormula.AT_LEAST_ONE:
            self.__addAtLeastOneConstraint(literals, weight)
        else:
            raise AttributeError('Unknown cctype value: %s' % str(cctype))


    #
    # Override (See base class specification)
    def isHardClause( self, clause ):
        return clause in self.hard_clauses

    #
    #
    def __addClause( self, weight, clause):
        # Repeated clauses can have greater value than top
        if type(clause) != frozenset:
            clause = frozenset(clause) # Dictionaries need it

        # If the clause is hard leave it as is
        if clause not in self.hard_clauses:
            # Restrict values to be at most top
            w = min(self.clauses_weights.get(clause, 0) + weight, self.top)

            if clause in self.soft_clauses:
                if w == self.top:
                    self.hard_clauses.add(clause)
                    self.soft_clauses.remove(clause)
            else:
                if w == self.top:
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
        self.__addClause( weight, clause )

    #
    #
    def __addAtMostOneConstraint(self, literals, weight):
        if type(literals) != list:
            literals = list(literals)


        for i in xrange( len(literals)-1 ):
            for j in xrange(i+1, len(literals) ):
                clause = frozenset( (-literals[i], -literals[j]) )
                self.__addClause( weight, clause )

    #
    #
    def __newVariable(self):
        self.nvars += 1
        return self.nvars
