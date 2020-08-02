from bparser.boolparser import BooleanParser
from bparser.tseitin_generator import TseitinFormula


def main():
    formulas = {
        '(a || b) && c || !(d && e)': 'string',
        '(!(p && (q || !r)))': 'string',
        '(a && b) || (a && !c)': 'string',
        '(a && b) or ((c || d) and e)': 'string',
        'src/data/simple_dnf_0.dnf': 'dnf_file',
        'src/data/formula.txt': 'txt_file'
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


if __name__ == "__main__":
    main()
