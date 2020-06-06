from parser.boolparser import BooleanParser
from parser.tseitin_generator import TseitinFormula

formulas = [
    '(a || b) && c || !(d && e)',
    # '(!(p && (q || !r)))',
    # '(a && b) || (a && !c)',
    # '(a && b) or ((c || d) and e)'
]

for test_id, formula in enumerate(formulas, start=0):
    print("\n=============== TEST %d ===============\n" % (test_id))
    f = TseitinFormula(formulas[test_id])
    f.toCNF()
    print(f.toString())

    if test_id == 0:
        f.exportToFile("simple_cnf")

    f.solve()
    print(f.getTermAssignment())
