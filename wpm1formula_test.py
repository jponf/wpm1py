# -*- coding: utf-8 -*-

import sys
import unittest
import wpm1formula

class TestFormula(unittest.TestCase):

    num_vars = 3
    inf = 16

    clauses = [ (1, [-1, 2, 3]), 
                (2, [1, 2, -3]),                
                (4, [1, -2, 3]),
                (4, [1, 2 ,3]), 
                (5, [-1, -2, 3]),
                (16, [1, -2, -3]),
                (16, [-1, -2, -3]) ]

    #
    #   Sets up the formula, before any test
    #
    def setUp(self):
        self.formula = wpm1formula.Formula( self.num_vars, self.inf, 
                                                                self.clauses )

    #
    #   Tests if we can retrieve the hard clauses as an iterable set
    #
    def test_getHardClausesFormula( self ):
        hclauses = set( [frozenset([1, -2, -3]), frozenset([-1, -2, -3])] )
        expected = (self.num_vars, hclauses)

        self.assertEqual(expected, self.formula.getHardClausesFormula())

    #
    #   Tests if we can retrieve a formula filled with clauses which weight is
    #   equals or bigger than a given value
    #
    def test_getFormulaWithMinWeight( self ):
        eclauses = set( [frozenset([1, -2, 3]),
                         frozenset([1, 2 ,3]),
                         frozenset([-1, -2, 3]),
                         frozenset([1, -2, -3]),
                         frozenset([-1, -2, -3])] )
        expected = (self.num_vars, eclauses)        

        self.assertEqual(expected, self.formula.getFormulaWithMinWeight(3))

    #
    #   Max weight in the formula less than an specified upper bound
    #
    def test_getMaxWeightLessThan( self ):
        self.assertEqual(1, self.formula.getMaxWeightLessThan(2))

    #
    #   Tests if we can retrieve the minimum weight of a set of clauses
    #
    def test_getMinWeightOfClauses( self ):
        clauses = set( [frozenset([1, -2, 3]),
                        frozenset([-1, -2, 3]),
                        frozenset([-1, -2, -3])] )

        self.assertEqual(4, self.formula.getMinWeightOfClauses(clauses) )

    #
    #   
    #
    def test_isHardClause_with_a_hard_clause( self ):
        clause = frozenset([-1, -2, -3])

        self.assertTrue( self.formula.isHardClause(clause) )

    #
    #
    #
    def test_isHardClause_with_a_soft_clause( self ):
        clause = frozenset([1, -2, 3])

        self.assertFalse( self.formula.isHardClause(clause) )


#
#
if __name__ == '__main__':
    unittest.main()