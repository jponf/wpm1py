# -*- coding: utf-8 -*-

import sys
import unittest
import formula

class TestFormula(unittest.TestCase):

    num_vars = 3
    inf = 18

    clauses = [ (1, [-1, 2, 3]), (1, [2, -3, 1]), 
                (1, [-3, 2, 1]), (1, [-2, 3, 1]),
                (2, [3, 1, 2]), (2, [3, 2, 1]),
                (2, [-2, -1, -3]), (2, [3, -1, -2]),
                (3, [1, 3, -2]), (3, [-2, -1, 3]), 
                (18, [1, -2, -3]), (18, [-3, -1, -2]) ]


    #
    #   Sets up the formula, before any test
    #
    def setUp(self):
        self.formula = formula.Formula( self.num_vars, self.inf, self.clauses )

    #
    #   Test if we can retrieve the hard clauses as an iterable set
    #
    def test_getHardClausesFormula( self ):
        hclauses = set( [frozenset([1, -2, -3]), frozenset([-3, -1, -2])] )
        expected = (self.num_vars, hclauses)
        self.assertEqual(expected, self.formula.getHardClausesFormula())


#
#
if __name__ == '__main__':
    unittest.main()