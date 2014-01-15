# -*- coding: utf-8 -*-

import sys


class WCNFParser:

    TYPE_UNKNOWN = 0
    TYPE_CNF = -1
    TYPE_WEIGHTED = -2
    TYPE_WEIGHTED_PARTIAL = -3   # Same parameters as partial

    def __init__(self, infile):

        self.infile = infile

        self.formula_type = WCNFParser.TYPE_UNKNOWN

        self.clauses = []
        self.num_clauses = 0
        self.num_vars = 0
        self.top = 1

    def parse(self):
        """parse(): ( num_vars: int, top:int, clauses: set() )

        Parses the file specified on the __init__ method.

        Returns:
            - num_vars: Formula's range of variables (specified on 'p' line)
            - top: Hard clauses' weight
            - clauses: A set filled with pairs (weight: int, clause: set)
        """

        # File hasn't been parsed before
        if not self.clauses:

            # Parse file
            try:
                for nline, line in enumerate(self.infile):
                    line = line.strip()

                    if not line or self.__isComment(line):
                        continue

                    if self.__isParametersLine(line):
                        self.__parseParametersLine(line)

                    else:
                        self.__parseClause(line)

                # Compare if the amount of parsed clauses with the specified
                # on the parameters line
                if self.num_clauses != len(self.clauses):
                    raise Exception(
                        '[WCNFParser] The amount of parsed clauses '
                        'does not match the specified on the parameters line')

            except SyntaxError as e:
                sys.stderr.write(
                    '[WCNFParser] Error parsing file "%s" (%d): %s\n'
                    % (self.infile.name, nline, str(e)))
                raise e

        return self.num_vars, self.top, self.clauses

    #
    #
    def __parseParametersLine(self, line):

        line_values = line.split()

        if len(line_values) < 4 or len(line_values) > 5:
            raise SyntaxError(
                '[WCNFParser] Parameters line must have 4 elements for cnf '
                'format and between 4 and 5 for wcnf format')

        if self.__isCNF(line_values):
            self.__parseCNFParameters(line_values)

        elif self.__isWCNF(line_values):
            self.__parseWCNFParameters(line_values)

    #
    #
    def __parseCNFParameters(self, line_values):

        if len(line_values) != 4:
            raise SyntaxError(
                '[WCNFParser] Parameters line for cnf format must '
                'have 4 elements: p cnf nbvar nbclauses')

        self.num_vars = int(line_values[2])
        self.num_clauses = int(line_values[3])

        self.formula_type = WCNFParser.TYPE_CNF

    #
    #
    def __parseWCNFParameters(self, line_values):

        if len(line_values) == 4:
            self.formula_type = WCNFParser.TYPE_WEIGHTED
        else:
            self.formula_type = WCNFParser.TYPE_WEIGHTED_PARTIAL
            self.top = int(line_values[4])

        self.num_vars = int(line_values[2])
        self.num_clauses = int(line_values[3])

    def __parseClause(self, line):

        values = map(int, line.split())

        # Clause weight
        weight = 0
        if self.formula_type == WCNFParser.TYPE_CNF:
            weight = 1
        else:
            if len(values) < 3:
                raise SyntaxError(
                    '[WCNFParser] Weighted clause line must have '
                    'more than 2 elements, at least [weight one_lit 0]')

            # Get and check weight
            weight = values[0]
            del values[0]

            if weight <= 0:
                raise SyntaxError(
                    '[WCNFParser] Clause\'s weight must be '
                    'greater than 0')

            # If it is only weighted (without hard clauses) set top as the
            # sum of all the weights plus one
            if self.formula_type == WCNFParser.TYPE_WEIGHTED:
                self.top += weight

        # Parse the rest of the clause
        clause = set()

        for lit in values:
            if lit == 0:
                self.clauses.append((weight, clause))
                clause = None
            else:
                clause.add(lit)

                if lit < -self.num_vars or lit > self.num_vars:
                    raise SyntaxError(
                        '[WCNFParser] Invalid literal %d, it must '
                        'be in range +/-[1, %d].' % (lit, self.num_vars))

        if clause:
            raise SyntaxError('Trailing 0 not found')

    #
    #
    def __isComment(self, line):
        return line[0] == 'c'

    #
    #
    def __isParametersLine(self, line):
        return line[0] == 'p'

    #
    #
    def __isCNF(self, line_values):
        return line_values[1].lower() == 'cnf'

    #
    #
    def __isWCNF(self, line_values):
        return line_values[1].lower() == 'wcnf'
