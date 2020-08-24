from bparser.boolparser import BooleanParser
from solver.SATSolver import SATSolver
from utils import tseitin_conversions as tc
from collections import deque
import os

# TODO: add debug field, there is no reason to pass debug mode to every method
# TODO: test this on large files


class TseitinFormula:
    def __init__(self, formula, formula_format="string", convert_to_cnf=True,
                 export_to_file=False, export_file_name="data", debug=False):

        if formula_format == 'string':
            self.original_formula = formula
        elif formula_format == 'file':
            self.original_formula = self.getFormulaFromFile(
                formula, debug=debug)
        else:
            raise RuntimeError(
                "Unsupported formula format. You can use one of following options: string, file.")

        # parse tree
        if debug:
            print("Parsing formula...")
        self.tree = BooleanParser(self.original_formula)

        self.tseitin_formula = ''
        self.root = self.tree.root

        # list of all clauses based on tree
        # every clause is a list, where:
        # id = 0: first term or index of another clause
        # id = 1: operator id
        # id = 2: second term or index of another clause
        self.clauses = []
        self.original_terms = []
        # list of all terms in expression
        self.terms = {}

        # ids of last clause for left and right tree, it is necessary to get the last clause
        self.last_clause_ids = []

        # formatted dict of all clauses
        # keys: clause name, for example phi0
        # values: dict with keys 'first_term', 'second_term', 'operator', 'is_negated'
        self.clause_map = {}
        self.is_valid = True
        self.terms_assignment = {}
        self.execution_time_str = ''

        if convert_to_cnf:
            self.toCNF(debug=debug)

            # if export_to_file:
            #     self.exportToFile(export_file_name)

    def toCNF(self, debug=False):
        if debug:
            print("Converting data to Tseitin formula...")

        self.toTseitinClausesWithStack(self.root)
        self.getTseitinClauses()
        self.setTseitinFormula()

        if debug:
            print("Converting complete!")

    def toTseitinClauses(self, prev_node, node):
        var_token = self.tree.tokenizer.getToken('var')

        if node.left != None and node.left.tokenType != var_token:
            self.toTseitinClauses(node, node.left)

        if node.right != None and node.right.tokenType != var_token:
            self.toTseitinClauses(node, node.right)

        # build clause
        clause = []
        if node == self.root:

            clause = [
                None, node.tokenType, None, node.negate
            ]

            var_token = self.tree.tokenizer.getToken('var')

            # if left/right child of root is a term then last_clause_ids may be incomplete
            if len(self.last_clause_ids) != 2:
                # debug purposes only
                # print("IDS: ", self.last_clause_ids,
                #       node.left.tokenType, node.left.value, node.right.tokenType, node.right.value)

                if node.left.negate == True or node.left.tokenType == var_token:
                    # left child is a term
                    if node.left.negate:
                        self.clauses.append(
                            self.getNegatedTermClause(node.left))
                        clause[0] = len(self.clauses)-1
                    else:
                        clause[0] = node.left.value
                else:
                    # left child is an operator
                    clause[0] = self.last_clause_ids[0]

                if node.right.negate == True or node.right.tokenType == var_token:
                    # right child is a term

                    if node.right.negate:
                        self.clauses.append(
                            self.getNegatedTermClause(node.right))
                        clause[2] = len(self.clauses)-1
                    else:
                        clause[2] = node.right.value
                else:
                    # right child is a operator
                    clause[2] = self.last_clause_ids[0]

            else:
                # both leaves of root node are operators
                clause[0] = self.last_clause_ids[0]
                clause[2] = self.last_clause_ids[1]

        else:
            if node.left.value == None:
                clause.append(len(self.clauses)-1)
            else:
                if node.left.negate:
                    self.clauses.append(self.getNegatedTermClause(node.left))
                    clause.append(len(self.clauses)-1)
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

    # TODO: rename to: toTseitinClauses
    def toTseitinClausesWithStack(self, node):
        var_token = self.tree.tokenizer.getToken('var')
        nodestack = deque()
        current = node
        previous = None

        while True:
            while current != None and current.tokenType != var_token:
                if current.right != None and current.right.tokenType != var_token:
                    nodestack.append((current, current.right))
                nodestack.append((previous, current))

                previous = current
                current = current.left

            (previous, current) = nodestack.pop()

            if current.right != None and current.right.tokenType != var_token and len(nodestack) > 0 and nodestack[-1][1] == current.right:
                nodestack.pop()
                nodestack.append((previous, current))
                previous = current
                current = current.right
            else:
                #########process current######################
                # build clause
                clause = []

                if current == self.root:
                    clause = [None, current.tokenType, None, current.negate]

                    if len(self.last_clause_ids) != 2:
                        if current.left.negate == True or current.left.tokenType == var_token:
                            # left child is a term
                            if current.left.negate:
                                self.clauses.append(
                                    self.getNegatedTermClause(current.left))
                                clause[0] = len(self.clauses)-1
                            else:
                                clause[0] = current.left.value
                        else:
                            # left child is an operator
                            clause[0] = self.last_clause_ids[0]

                        if current.right.negate == True or current.right.tokenType == var_token:
                            # right child is a term
                            if current.right.negate:
                                self.clauses.append(
                                    self.getNegatedTermClause(current.right))
                                clause[2] = len(self.clauses)-1
                            else:
                                clause[2] = current.right.value
                        else:
                            # right child is an operator
                            clause[2] = self.last_clause_ids[0]
                    else:
                        # both leaves of root node are operators
                        clause[0] = self.last_clause_ids[0]
                        clause[2] = self.last_clause_ids[1]
                else:
                    if current.left.value == None:
                        clause.append(len(self.clauses)-1)
                    else:
                        if current.left.negate:
                            self.clauses.append(
                                self.getNegatedTermClause(current.left))
                            clause.append(len(self.clauses)-1)
                        else:
                            clause.append(current.left.value)

                    clause.append(current.tokenType)

                    if current.right.value == None:
                        clause.append(len(self.clauses)-1)
                    else:
                        if current.right.negate:
                            self.clauses.append(
                                self.getNegatedTermClause(current.right))
                            clause.append(len(self.clauses)-1)
                        else:
                            clause.append(current.right.value)

                    clause.append(current.negate)
                self.clauses.append(clause)

                if previous == self.root:
                    self.last_clause_ids.append(len(self.clauses)-1)

                ############end process current####################
                previous = current
                current = None

            if len(nodestack) <= 0:
                break

    def getNegatedTermClause(self, node):
        token = self.tree.tokenizer.getToken('not')
        return [
            node.value, token, None, False
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
                self.original_terms.append(first_term)

            if isinstance(clause[2], int):
                second_term = "phi" + str(clause[2])
            else:
                second_term = clause[2]
                self.original_terms.append(second_term)

            operator, is_negated = clause[1], clause[3]
            if operator == 'AND' and is_negated:
                operator = "NAND"
            elif operator == 'OR' and is_negated:
                operator = 'NOR'

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

            if operator == 'NOT':
                term_list = [definition['first_term'], clause]
            else:
                term_list = [definition['first_term'],
                             definition['second_term'], clause]
            terms.extend(term_list)

            if operator == 'AND':
                clauses.extend(tc.getTseitinAndClause(term_list))
            elif operator == 'NAND':
                clauses.extend(tc.getTseitinNandClause(term_list))
            elif operator == 'OR':
                clauses.extend(tc.getTseitinOrClause(term_list))
            elif operator == 'NOR':
                clauses.extend(tc.getTseitinNorClause(term_list))
            elif operator == 'NOT':
                clauses.extend(tc.getTseitinNotClause(term_list))

        # append the last variable as clause
        clauses.append([clause])

        # removes duplicates from terms list
        self.terms = dict.fromkeys(terms)
        idx = 0
        for t in self.terms:
            self.terms[t] = idx
            idx += 1
        self.clauses = clauses

        self.tseitin_formula = self.getTseitinFormulaStr(split=False)

    def getTseitinFormulaStr(self, split=True):
        tseitin_formula = []
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

            tseitin_formula.append(term_str + " and ")

        tseitin_formula[-1] = tseitin_formula[-1][:-5]
        if split:
            for part in tseitin_formula:
                part = part.replace("and ", "and\n")

        return "".join(tseitin_formula)

    def toString(self):
        return self.tseitin_formula

    # TODO: fix this method, useless with large formulas
    # export Tseitin CNF form to .cnf file
    def exportToFile(self, file_name):
        clause_num = len(self.clauses)
        term_num = len(self.terms)

        script_path = os.path.dirname(__file__)
        path_list = script_path.split(os.sep)
        script_directory = path_list[0:len(path_list)-1]
        rel_path = "data/" + file_name + ".cnf"
        path = "/".join(script_directory) + "/" + rel_path
        with open(path, "w+") as f:

            f.write("c  " + file_name + ".cnf\n")
            f.write("c\n")
            f.write("p cnf %d %d\n" % (term_num, clause_num))

            for clause in self.clauses:
                formatted_clause_list = []
                for idx, term in enumerate(clause):
                    if term == -1:
                        continue

                    term_id = self.terms[term] + 1
                    if idx > 0 and clause[idx-1] == -1:
                        term_id *= -1

                    formatted_clause_list.append(term_id)

                formatted_clause_list.append(0)
                clause_str = ' '.join(map(str, formatted_clause_list))
                clause_str += '\n'

                f.write(clause_str)

    # TODO: this method should show messages depends on debug mode
    def solve(self, solver_name='m22', return_all_assignments=True, use_timer=True):
        solver_data = SATSolver(
            self.terms, self.clauses).solve(solver_name, return_all_assignments, use_timer)

        self.execution_time_str = solver_data['execution_time']
        self.terms_assignment = solver_data['terms_assignment']

    def getTermAssignment(self, only_original=True):
        terms_assignment = []

        for assignment in self.terms_assignment:
            part_assignment = {}

            for term, term_value in assignment.items():
                if only_original and term in self.original_terms:
                    part_assignment[term] = term_value
                elif only_original is False:
                    part_assignment[term] = term_value
            terms_assignment.append(part_assignment)

        return terms_assignment

    def getFormulaFromFile(self, filepath, debug=True):
        _, file = os.path.split(filepath)
        extension = file.split(".")[-1]

        if extension not in ["txt", "cnf", "dnf"]:
            raise RuntimeError(
                f'Not supported file extension: \'{extension}\'...')

        if debug:
            print(f'Loading data from file: \'{file}\'...')

        if extension == "txt":
            formula = self.getFromulaFromTxt(filepath)
        elif extension in ["cnf", "dnf"]:
            formula = self.getFormulaFromDIMAC(filepath)

        if debug:
            print("The data has been loaded!")

        return formula

    def getFormulaFromDIMAC(self, filepath):
        with open(filepath, 'r') as file:
            initial_lines = True
            subformulas_list = []
            for line in file:
                subformula = ""
                if initial_lines:
                    # skip comment lines
                    if line[0] == 'c':
                        continue
                    # check if file is truly a dnf or cnf file inside and switch flag to formula processing
                    elif line[0] == 'p' and line[2:5] in ["cnf", "dnf"]:
                        initial_lines = False
                    else:
                        raise RuntimeError(
                            "Intial file lines do not follow DNF or CNF syntax.")
                else:
                    # variable used to concatenate digits of variable numbers higher than 9
                    variable_number = ""
                    try_to_place_and = False
                    expect_number = False
                    expect_minus_or_number = False
                    for character in line:
                        # check if loaded character is of expected type
                        if expect_minus_or_number and not (character == '-' or character.isdigit()):
                            raise RuntimeError("Syntax error in clause line.")
                        else:
                            expect_minus_or_number = False

                        if expect_number and not character.isdigit():
                            raise RuntimeError("Syntax error in clause line.")
                        else:
                            expect_number = False

                        # if there was an ongoing concatenation of digits but next character is not digit anymore
                        if variable_number != "" and not character.isdigit():
                            # it should be whitespace, if so, add a variable called userdefX, where X is concatenated number, to the formula
                            if character != ' ':
                                raise RuntimeError(
                                    "Syntax error in clause line.")
                            subformula = subformula + " userdef" + variable_number + " "
                            variable_number = ""

                        # if the whitespace that caused "and placing" was before next variable and not line-ending zero, the placing should happen
                        if try_to_place_and and character != '0':
                            subformula += " and "
                        try_to_place_and = False

                        if character == '-':
                            subformula += " not "
                            # minus should be followed by variable number
                            expect_number = True
                        elif character == ' ':
                            try_to_place_and = True
                            # whitespace should be followed by minus, variable number or line-ending zero
                            expect_minus_or_number = True
                        elif character.isdigit():
                            if character == '0' and variable_number == "":
                                subformulas_list.append(subformula)
                                break
                            variable_number += character
                        else:
                            raise RuntimeError("Syntax error in clause line.")

        # while returning, cut off the ending containing " or " caused by the last endline
        return " or ".join(subformulas_list)

    # TODO: read data using with statement
    # TODO: better reading method, now it reads only one line
    # TODO: better exception handling
    def getFromulaFromTxt(self, filepath):

        txt_file = open(filepath, 'r')

        formula = ""
        for line in txt_file:
            formula = line
            break

        txt_file.close()

        return formula

    # TODO: there is no way to generate report for large formulas, export result to file
    # TODO: show warning to user
    def getSolverReport(self):
        original_terms = list(set(self.original_terms))
        original_terms = [x for x in original_terms if x != None]

        report_str = "Original formula:\n" + self.original_formula + \
            "\n\nTseitin formula:\n" + self.tseitin_formula + \
            "\n\nOriginal number of terms:\n" + str(len(original_terms)) + \
            "\n\nTseitin number of terms:\n" + str(len(self.terms)) + \
            "\n\nExecution time:\n" + self.execution_time_str + \
            "\n\nTerms assignment:\n"

        for terms_assignment in self.getTermAssignment():
            report_str += str(terms_assignment) + "\n"

        return report_str

    # TODO: remove when development finished
    def diagnostic(self):
        original_terms = list(set(self.original_terms))
        original_terms = [x for x in original_terms if x != None]

        print(len(original_terms))
        print(len(self.original_formula))
