from boolparser import BooleanParser, TokenType
import tseitin_conversions as tc

class TseitinFormula:
    root = None

    # list of all clauses based on tree
    # every clause is a list, where:
    # id = 0: first term or index of another clause
    # id = 1: operator id
    # id = 2: second term or index of another clause
    clauses = []

    # formatted dict of all clauses
    # keys: clause name, for example phi0
    # values: dict with keys 'first_term', 'second_term', 'operator', 'is_negated'
    clause_map = {}

    # ids of last clause for left and right tree, it is necessary to get the last clause
    last_clause_ids = []

    # list of all terms in expression
    terms = []
    
    # ! FIXME: temporary solution
    operator_decoding = {6: "and", 7: "or", 8: "not"}

    def __init__ (self, formula):
        tree = BooleanParser(formula)
        self.root = tree.root
        self.clauses = []
        self.last_clause_ids = []
        self.clause_map = {}

    def toCNF (self):        
        self.toTseitinClauses(None, self.root)
        self.getTseitinClauses()
        self.setTseitinFormula()

    def toTseitinClauses(self, prev_node, node):
        if node.left != None and node.left.tokenType != TokenType.VAR:
            self.toTseitinClauses(node, node.left)
        
        if node.right != None and node.right.tokenType != TokenType.VAR:
            self.toTseitinClauses(node, node.right)

        # build clause
        clause = []
        if node == self.root:
            clause = [
                None, node.tokenType, None, node.negate
            ]

            # if left/right child of root is a term then last_clause_ids may be incomplete
            if len(self.last_clause_ids) != 2:
                if node.left.tokenType == 1:
                    # left child is a term
                    clause[0] = node.left.value
                else:
                    # left child is a operator
                    clause[0] = self.last_clause_ids[0]

                if node.right.tokenType == 1:
                    # right child is a term
                    clause[2] = node.right.value
                else:
                    # right child is a operator
                    clause[2] = self.last_clause_ids[0]

            # both leaves of root node are operators
            else:
                clause[0] = self.last_clause_ids[0]
                clause[2] = self.last_clause_ids[1]

        else:
            if node.left.value == None:
                clause.append(len(self.clauses)-1)
            else:
                if node.left.negate:
                    clause.append(self.getNegatedTermClause(node.left))
                else:
                    clause.append(node.left.value)

            clause.append(node.tokenType)

            if node.right.value == None:
                clause.append(len(self.clauses)-1)
            else:
                if node.right.negate:
                    self.clauses.append(self.getNegatedTermClause(node.right))
                    clause.append(len(self.clauses)-1)
                else:
                    clause.append(node.right.value)

            clause.append(node.negate)

        self.clauses.append(clause)

        if prev_node == self.root:
            self.last_clause_ids.append(len(self.clauses)-1)
        

    def getNegatedTermClause(self, node):
        # TODO: second element should be 'not' token type
        return [
            node.value, 8, None, False
        ]

    def getTseitinClauses(self):      
        i = 0
        for clause in self.clauses:
            logic_var = "phi" + str(i)
            first_term, second_term = "", ""

            if isinstance(clause[0], int):
                first_term = "phi" + str(clause[0])
            else:
                first_term = clause[0]

            if isinstance(clause[2], int):
                second_term = "phi" + str(clause[2])
            else:
                second_term = clause[2]

            # ! FIXME: this should be get from some kind of map or sth
            # TODO: move to separate method
            operator, is_negated = clause[1], clause[3]
            if operator == 6 and is_negated:
                operator = "nand"
            elif operator == 6:
                operator = "and"
            elif operator == 7 and is_negated:
                operator = 'nor'
            elif operator == 7:
                operator = 'or'
            elif operator == 8:
                operator = 'not'
         
            self.clause_map[logic_var] = {
                "first_term": first_term,
                "second_term": second_term,
                "operator": operator
            }

            i += 1
    
    def setTseitinFormula(self):
        clauses = []
        terms = []

        for clause, definition in self.clause_map.items():
            operator = definition['operator']

            if operator == 'not':
                term_list = [definition['first_term'], clause]
            else:
                term_list = [definition['first_term'], definition['second_term'], clause]            
            terms.extend(term_list)

            if operator == 'and':
                clauses.extend(tc.getTseitinAndClause(term_list))
            elif operator == 'nand':
                clauses.extend(tc.getTseitinNandClause(term_list))
            elif operator == 'or':
                clauses.extend(tc.getTseitinOrClause(term_list))
            elif operator == 'or':
                clauses.extend(tc.getTseitinNorClause(term_list))
            elif operator == 'not':
                clauses.extend(tc.getTseitinNotClause(term_list))

        # append the last variable as clause
        clauses.append([clause])
        
        self.terms =list(dict.fromkeys(terms))
        self.clauses = clauses

    def toString(self):
        tseitin_formula = ""
        for clause in self.clauses:
            term_str = "("

            for term in clause:
                if term == -1:
                    term_str += "!"
                else:
                    term_str = term_str + term + " or "

            # remove last 'or'
            term_str = term_str[:-4]
            term_str = term_str + ")"

            tseitin_formula = tseitin_formula + term_str + " and "
        
        return tseitin_formula[:-5]

    # export Tseitin CNF form to .cnf file
    def exportToFile(self):
        clause_num = len(self.clauses)
        term_num = len(self.terms)

        f= open("simple_cnf.cnf", "w+")
        f.write("c  simple_cnf.cnf\n")
        f.write("c\n")
        f.write("p cnf %d %d\n" % (term_num, clause_num))

        for clause in self.clauses:
            formatted_clause_list = []
            for idx, term in enumerate(clause):
                if term == -1:
                    continue

                term_id = self.terms.index(term)
                if idx > 0 and clause[idx-1] == -1:
                    term_id *= -1
                
                formatted_clause_list.append(term_id)
            
            formatted_clause_list.append(0)
            clause_str = ' '.join(map(str, formatted_clause_list))
            clause_str += '\n'

            f.write(clause_str)
        
        f.close()