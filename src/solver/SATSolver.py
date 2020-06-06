from pysat.solvers import Solver


class SATSolver:
    def __init__(self, solver_name, terms, clauses):
        self.terms = terms
        self.clauses = clauses
        self.solver = Solver(name=solver_name)
        self.__initSolver()

    def __del__(self):
        self.solver.delete()

    def __initSolver(self):
        for clause in self.clauses:
            formatted_clause_list = []
            for idx, term in enumerate(clause):
                if term == -1:
                    continue

                term_id = self.terms.index(term) + 1
                if idx > 0 and clause[idx-1] == -1:
                    term_id *= -1

                formatted_clause_list.append(term_id)

            self.solver.add_clause(formatted_clause_list)

    def solve(self):
        result = {}

        is_valid = self.solver.solve()
        result['is_valid'] = is_valid

        term_values = self.solver.get_model()
        terms_assignment = {}
        for (term, value) in zip(self.terms, term_values):
            terms_assignment[term] = 1 if value > 0 else 0
        result['terms_assignment'] = terms_assignment

        return result
