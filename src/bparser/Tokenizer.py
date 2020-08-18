# TODO: some of expression needs parenthesis on the beginning and the end, there is need to add additional validation
class Tokenizer:
    def __init__(self, exp):
        # loogic formula
        self.expression = exp

        # list of all found tokens in exp
        self.tokens = []
        self.tokenTypes = []
        self.i = 0

        self.tokenMap = {
            'VAL': 'VAL', 'val': 'VAL', False: 'VAL', True: 'VAL',
            'VAR': 'VAR', 'var': 'VAR',
            'EQ': 'EQ', 'eq': 'EQ', '==': 'EQ',
            'NEQ': 'NEQ', 'neq': 'NEQ', '!=': 'NEQ', '~=': 'NEQ',
            'LP': 'LP', '(': 'LP', 'lp': 'LP',
            'RP': 'RP', ')': 'RP', 'rp': 'RP',
            'AND': 'AND', 'and': 'AND', '&&': 'AND',
            'OR': 'OR', 'or': 'OR', '||': 'OR',
            'NOT': 'NOT', 'not': 'NOT', '~': 'NOT', '!': 'NOT'
        }

    def getToken(self, token):
        return self.tokenMap[token]

    def isOperator(self, token):
        return token in self.tokenMap.keys() and self.getToken(token) in ['AND', 'OR', 'NOT']

    def next(self):
        self.i += 1
        return self.tokens[self.i-1]

    def prev(self):
        self.i -= 1

        if self.i < 0:
            raise Exception("There is no previous elements")
        return self.tokens[self.i]

    def peek(self):
        if self.hasNext():
            return self.tokens[self.i]
        else:
            return "formula end"

    def hasNext(self):
        return self.i < len(self.tokens)

    def nextTokenType(self):
        return self.tokenTypes[self.i]

    def nextTokenTypeIsOperator(self):
        t = self.tokenTypes[self.i]
        return t == 'EQ' or t == 'NEQ'

    def tokenize(self):
        import re
        reg = re.compile(
            r'(\btrue\b|\bfalse\b|\bTrue\b|\bFalse\b|\bAND\b|\band\b|&&|\bOR\b|\bor\b|\|\||\bNOT\b|\bnot\b|~|!|~=|!=|==|\(|\))')

        # every symbol in the input expression should be separate element on list
        self.tokens = reg.split(self.expression)

        # remove '=' symbol from expression if it appears with '!'
        for idx in range(len(self.tokens)):
            if self.tokens[idx] == '!' and re.match('=.*', self.tokens[idx+1]):
                self.tokens[idx] = '!='
                self.tokens[idx+1] = self.tokens[idx+1][1:]
            elif self.tokens[idx] == '~' and re.match('=.*', self.tokens[idx+1]):
                self.tokens[idx] = '~='
                self.tokens[idx+1] = self.tokens[idx+1][1:]

        # remove white characters
        self.tokens = [t.strip() for t in self.tokens if t.strip() != '']

        for t in self.tokens:
            if t == 'False' or t == 'false' or t == '0':
                t = False
            elif t == 'True' or t == 'true' or t == '1':
                t = True
            if not self.isOperator(t) and not (t == True or t == False) and re.search('^[a-zA-Z_]+[0-9]*$', t):
                self.tokenTypes.append(self.getToken('var'))
            else:
                self.tokenTypes.append(self.getToken(t))
