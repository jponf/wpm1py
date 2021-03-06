# -*- coding: utf-8 -*-


class MSatFormula:
    """Stores all the necessary information of a Weighted SAT Formula

    Clauses should be represented as frozensets to avoid modifications.
    """

    TOP = -1
    EXACTLY_ONE = -2
    AT_MOST_ONE = -3
    AT_LEAST_ONE = -4

    #
    #
    def getHardClausesFormula(self):
        """getHardClausesFormula(): (nvars: int, clauses: set)

        Returns a tuple with 2 components:
            - nvars: At least the value of the highest variable or greater

            - clauses: A set filled with all the hardclauses
                f.e: set([ set([1,2,-4,5]), set([1,5,-7,8]) )

                For optimization reasons, this set can be a reference to the
                internal set of clauses. Do not modify it!
        """
        raise NotImplementedError(
            'getHardClausesFormula(). Abstract method')

    def getFormulaWithMinWeight(self, min_weight):
        """getFormulaWithMinWeight(min_weight: int): (nvars: int, clauses: set)

        Returns a tuple with 2 components:
            - nvars: At least the value of the highest variable or greater

            - clauses: A set filled with all the clauses with weight is equals
                       or greater than min_weight
        """
        raise NotImplementedError(
            'getFormulaWithMinWeight( min_weight ). Abstract method')

    def getMaxWeightLessThan(self, upper_bound):
        """maxWeightLessThan(upper_bound:int): int

        Parameters:

            - upper_bound: must be a possitive integer > 0 or MSatFormula.TOP

        Returns the max weight in the formula, less than the specified upper
        bound.

        Raises:
            - ValueError if upper_bound is 0 or negative
        """
        raise NotImplementedError(
            'maxWeightLessThan( upper_bound ). Abstract method')

    def getMinWeightOfClauses(self, clauses):
        """minWeightOfClauses(clauses: []/set): int

        Returns the minimum weight of the specified clauses.

        Raises:
            - LookupError: If clauses contains a clause that doesn't belongs to
                            the formula
        """
        raise NotImplementedError(
            'minWeightOfClauses( clauses ). Abstract method')

    def relaxClause(self, clause, weight):
        """relaxClause(clause: set, weight: int): int

        Duplicates the given clause adding a new variable to the copy. The new
        clause will have the specified weight and the old one will have its old
        weight minus the new weight.

        If the old clause new weight is 0 then it is deleted.

        Returns the new variable added to the copy.

        Raises LookupError: If the specified clause doesn't belong to the
                            formula
        """
        raise NotImplementedError(
            'relaxClause( clause, weight ). Abstract method')

    def addCardinalityConstraint(self, literals, cctype, weight):
        """addCardinalityConstraint(literals: set, cctype: int, weight: int)

        Add the specified cardinality constraint 'cctype' to the given literals
        with the specified weight.

        - cctype: Must be one of the next MSatFormula 'constants'
            - MSatFormula.EXACTLY_ONE
            - MSatFormula.AT_MOST_ONE
            - MSatFormula.AT_LEAST_ONE

        - weight: Must be an integer greater than 0 or MSatFormula.TOP

        Raises
        """
        raise NotImplementedError(
            'addCardinalityConstraint( literals, cctype, weight ). '
            'Abstract method')

    def isHardClause(self, clause):
        """isHardClause(clause: set): bool

        Returns True if the specified clause is a hard clause. False otherwise.
        """
        raise NotImplementedError(
            'isHardClause( upper_bound ). Abstract method')
