from bparser.boolparser import BooleanParser
from bparser.tseitin_generator import TseitinFormula


def simple_tests():
    formulas = {
        '(a || b) && c || !(d && e)': 'string',
        '(!(p && (q || !r)))': 'string',
        '(a && b) || (a && !c)': 'string',
        '(a && b) or ((c || d) and e)': 'string',
        'src/data/simple_dnf_0.dnf': 'dnf_file',
        'src/data/formula.txt': 'txt_file',
        'a and !a': 'string',
        '!x1 and x2 or x1 and !x2 or !x2 and x3': 'string',
        '!a and a': 'string'
    }

    for test_id, (formula_value, formula_format) in enumerate(formulas.items()):
        print("\n=============== TEST %d ===============\n" % (test_id))

        file_name = "simple_cnf_" + str(test_id)
        formula = TseitinFormula(
            formula=formula_value, formula_format=formula_format, export_to_file=True, export_file_name=file_name)

        formula.solve(solver_name='m22',
                      return_all_assignments=False, use_timer=True)

        # only for debug purposes
        print(formula.getSolverReport())


def advanced_test():
    print("\n=============== ADVANCED TEST ===============\n")
    input_file_name = 'src/data/Analiza1-itox_vc1033.cnf'
    formula = TseitinFormula(formula=input_file_name,
                             formula_format='dnf_file', export_to_file=False)

    formula.solve(solver_name='m22',
                  return_all_assignments=False, use_timer=True)


if __name__ == "__main__":
    # tests for very simple formulas
    simple_tests()

    # tests for large formulas
    advanced_test()
