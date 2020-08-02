from bparser.boolparser import BooleanParser
from bparser.tseitin_generator import TseitinFormula


def main():
    formulas = [
        '(a || b) && c || !(d && e)',
        '(!(p && (q || !r)))',
        '(a && b) || (a && !c)',
        '(a && b) or ((c || d) and e)'
    ]

    for test_id, _ in enumerate(formulas, start=0):
        print("\n=============== TEST %d ===============\n" % (test_id))

        file_name = "simple_cnf_" + str(test_id)
        formula = TseitinFormula(
            formulas[test_id], convert_to_cnf=True, export_to_file=True,
            export_file_name=file_name)

        formula.solve(return_all_assignments=True)

        # only for debug purposes
        print(formulas[test_id])
        print(formula.toString())
        for terms_assignment in formula.getTermAssignment():
            print(terms_assignment)


if __name__ == "__main__":
    main()
