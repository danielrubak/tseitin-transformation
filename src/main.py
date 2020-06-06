from parser.boolparser import BooleanParser
from parser.tseitin_generator import TseitinFormula


def main():
    formulas = [
        '(a || b) && c || !(d && e)',
        '(!(p && (q || !r)))',
        '(a && b) || (a && !c)',
        '(a && b) or ((c || d) and e)'
    ]

    for test_id, formula in enumerate(formulas, start=0):
        print("\n=============== TEST %d ===============\n" % (test_id))
        formula = TseitinFormula(formulas[test_id],
                                 convert_to_cnf=True, export_to_file=True)
        formula.solve('glucose3')

        # only for debug purposes
        print(formula.toString())
        print(formula.getTermAssignment())
        print(formula.getTermAssignment(only_original=True))


if __name__ == "__main__":
    main()
