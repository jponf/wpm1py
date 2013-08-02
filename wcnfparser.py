# -*- coding: utf-8 -*-

#
#
def parse(file_path):

    num_vars = 0
    inf = 0
    clauses = []

    cnf_file = open(file_path, 'r')

    try:
        for nline, line in enumerate(cnf_file):
            line = line.strip()

            if not line or __isComment(line):
                continue

            lvalues = line.split()

            if lvalues[0] == 'p':
                if len(lvalues) != 5:
                    raise SyntaxError('Parameter line must have 5 parameters: '
                                    'p wcnf nbvar nbclauses top')

                if lvalues[1] != 'wcnf':
                    raise SyntaxError('Invalid format idetifier "%s'
                            % (lvalues[1]) )

                num_vars = int(lvalues[2])
                inf = int(lvalues[4])



            else:
                # Does not support multiple clauses per line
                # Weight
                weight = int(lvalues[0])
                del lvalues[0]

                # Clause
                values = map(int, lvalues)
                clause = set()

                for lit in values:
                    if lit == 0:
                        clauses.append( (weight, clause) )
                        clause = None

                    else:
                        clause.add(lit)

                        if lit < -num_vars or lit > num_vars:
                            raise SyntaxError('Invalid literal %d, '
                                'it must ve in range +/-[1, %d].' 
                                % (lit, num_vars) )
                if clause:
                    raise SyntaxError('Trailing 0 not found')

    except SyntaxError as e:
        sys.stderr.write('Error parsing file "%s" (%d): %s\n' %
                            (file_path, nline, str(e)) )
        raise e

    return num_vars, inf, clauses

#
#
def __isComment(line):
    """
    __isComment(line: str): bool

    - Returns True if the line is a CNF-DIMACS comment, False otherwise
    """
    return line[0] == 'c'