from pysat.solvers import Solver


class SATSolver:
    def __init__(self, terms, clauses):
        self.terms = terms
        self.clauses = []
        self.__initSolver(clauses)

    def __initSolver(self, clauses):
        for clause in clauses:
            part_clause_list = []
            for idx, term in enumerate(clause):
                if term == -1:
                    continue

                term_id = self.terms.index(term) + 1
                if idx > 0 and clause[idx-1] == -1:
                    term_id *= -1

                part_clause_list.append(term_id)

            self.clauses.append(part_clause_list)

    def solve(self, return_all_assignments=True):
        result = []

        with Solver(bootstrap_with=self.clauses) as solver:
            for model in solver.enum_models():
                terms_assignment = {}
                for (term, value) in zip(self.terms, model):
                    terms_assignment[term] = 1 if value > 0 else 0
                result.append(terms_assignment)

                if not return_all_assignments:
                    break

        return result
