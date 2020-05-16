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

# conversion for 'xor' operator
# c <-> a xor b => (!a or !b or !c) and (a or b or !c) and (a or !b or c) and (!a or b or c)

def getTseitinXorClause(term_list):
    a, b, c = term_list
    
    return [
        [-1, a, -1, b, -1, c],
        [a, b, -1, c],
        [a, -1, b, c],
        [-1, a, b, c]
    ]

# conversion for 'xnor' operator
# c <-> a xnor b => (!a or !b or c) and (a or b or c) and (a or !b or !c) and (!a or b or !c)
def getTseitinXnorClause(term_list):
    a, b, c = term_list

    return [
        [-1, a, -1, b, c],
        [a, b, c],
        [a, -1, b, -1, c],
        [-1, a, b, -1, c]
    ]

def getTseitinAndClauseStr(a, b, c):
    return f"(!{a} or !{b} or {c}) and ({a} or !{c}) and ({b} or !{c})"

def getTseitinNandClauseStr(a, b, c):
    return f"(!{a} or !{b} or !{c}) and ({a} or {c}) and ({b} or {c})"

def getTseitinOrClauseStr(a, b, c):
    return f"({a} or {b} or !{c}) and (!{a} or {c}) and (!{b} or {c})"

def getTseitinNorClauseStr(a, b, c):
    return f"({a} or {b} or {c}) and (!{a} or !{c}) and (!{b} or !{c})"

def getTseitinNotClauseStr(a, b):
    return f"(!{a} or !{b}) and ({a} or {b})"

def getTseitinXorClauseStr(a, b, c):
    return f"(!{a} or !{b} or !{c}) and ({a} or {b} or !{c}) and ({a} or !{b} or {c}) and (!{a} or {b} or {c})"

def getTseitinXnorClauseStr(a, b, c):
    return f"(!{a} or !{b} or {c}) and ({a} or {b} or {c}) and ({a} or !{b} or !{c}) and (!{a} or {b} or !{c})"