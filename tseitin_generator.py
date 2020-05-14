from boolparser import BooleanParser, TokenType
import tseitin_conversions as tc

class TseitinFormula:
    root = None

    # list of all clauses based on tree
    # every clause is a list, where:
    # id = 0: first term or index of another clause
    # id = 1: operator id
    # id = 2: second term or index of another clause
    # id = 3: is negated
    clauses = []

    # formatted dict of all clauses
    # keys: clause name, for example phi0
    # values: dict with keys 'first_term', 'second_term', 'operator', 'is_negated'
    clause_map = {}

    # ids of last clause for left and right tree, it is necessary to get the last clause
    last_clause_ids = []

    terms = []
    
    # ! FIXME: temporary solution
    operator_decoding = {6: "or", 7: "and"}

    def __init__ (self, formula):
        tree = BooleanParser(formula)
        self.root = tree.root
        self.clauses = []
        self.last_clause_ids = []

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
                self.last_clause_ids[0],
                node.tokenType,
                self.last_clause_ids[1],
                node.negate
            ]

        else:
            if node.left.value == None:
                clause.append(len(self.clauses)-1)
            else:
                clause.append(node.left.value)

            clause.append(node.tokenType)

            if node.right.value == None:
                clause.append(len(self.clauses)-1)
            else:
                clause.append(node.right.value)

            clause.append(node.negate)
        
        self.clauses.append(clause)

        if prev_node == self.root:
            self.last_clause_ids.append(len(self.clauses)-1)

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
         
            self.clause_map[logic_var] = {
                "first_term": first_term,
                "second_term": second_term,
                "operator": self.operator_decoding[clause[1]] ,
                "is_negated": clause[3]
            }

            i += 1
    
    def setTseitinFormula(self):
        clauses = []
        terms = []

        # TODO: 

        for clause, definition in self.clause_map.items():
            term_list = [clause, definition['first_term'], definition['second_term']]
            terms.extend(term_list)

            operator = definition['operator']
            if operator == 'and':
                clauses.extend(tc.getTseitinAndClause(term_list))
            elif operator == 'or':
                clauses.extend(tc.getTseitinOrClause(term_list))

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

    def exportToFile(self):
        clause_num = len(self.clauses)
        term_num = len(self.terms)

        print(clause_num, term_num)

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