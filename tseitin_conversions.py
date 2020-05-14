
def getTseitinAndClause(term_list):
    a, b, c = term_list
    
    return [
        [-1, a, -1, b, c],
        [a, -1, c],
        [b, -1, c]
    ]

def getTseitinOrClause(term_list):
    a, b, c = term_list
    
    return [
        [a, b, -1, c],
        [-1, a, c],
        [-1, b, c]
    ]

def getTseitinAndClauseStr(a, b, c):
    return f"(!{a} or !{b} or {c}) and ({a} or !{c}) and ({b} or !{c})"

def getTseitinOrClauseStr(a, b, c):
    return f"({a} or {b} or !{c}) and (!{a} or {c}) and (!{b} or {c})"