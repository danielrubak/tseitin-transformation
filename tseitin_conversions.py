# conversion for 'and' operator
# c <-> a and b => (!a or !b or c) and (a or !c) and (b or !c)
def getTseitinAndClause(term_list):
    a, b, c = term_list
    
    return [
        [-1, a, -1, b, c],
        [a, -1, c],
        [b, -1, c]
    ]

# conversion for 'nand' operator
# c <-> !(a and b) => (!a or !b or !c) and (a or c) and (b or c)
def getTseitinNandClause(term_list):
    a, b, c = term_list
    
    return [
        [-1, a, -1, b, -1, c],
        [a, c],
        [b, c]
    ]

# conversion for 'or' operator
# c <-> a or b => (a or b or !c) and (!a or c) and (!b or c)
def getTseitinOrClause(term_list):
    a, b, c = term_list
    
    return [
        [a, b, -1, c],
        [-1, a, c],
        [-1, b, c]
    ]

# conversion for 'nor' operator
# c <-> !(a or b) => (a or b or c) and (!a or !c) and (!b or !c)
def getTseitinNorClause(term_list):
    a, b, c = term_list
    
    return [
        [a, b, c],
        [-1, a, -1, c],
        [-1, b, -1, c]
    ]

# conversion for 'not' operator
# b <-> !a => (!a or !b) and (a or b)
def getTseitinNotClause(term_list):
    a, b = term_list

    return [
        [-1, a, -1, b],
        [a, b]
    ]

def getTseitinAndClauseStr(a, b, c):
    return f"(!{a} or !{b} or {c}) and ({a} or !{c}) and ({b} or !{c})"

def getTseitinOrClauseStr(a, b, c):
    return f"({a} or {b} or !{c}) and (!{a} or {c}) and (!{b} or {c})"