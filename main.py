from boolparser import BooleanParser, TokenType
from tseitin_generator import *

# var_dict={"a":True, "b":False, "c":False, "d":True, "e":True}
# p = BooleanParser('(a || b) && c || !(d && e)')
# p.printTree(p.root)
# print(p.evaluate(var_dict))
# print(p.toString())

formulas = [
    '(a || b) && c || !(d && e)',
    '(!(p && (q || !r)))',
    '(a && b) || (a && !c)'
]

f1 = TseitinFormula(formulas[0])
f1.toCNF()
print(f1.toString())
f1.exportToFile()

# f2 = TseitinFormula(formulas[1])
# f2.toCNF()

print("\n==============================\n")
f3 = TseitinFormula(formulas[2])
f3.toCNF()
print(f3.toString())