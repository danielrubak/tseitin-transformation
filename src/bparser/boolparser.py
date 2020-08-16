from bparser.Tokenizer import *

"""
Grammar:
{!}Expression --> AndTerm { OR AndTerm}+
AndTerm --> Condition { AND Condition}+
Condition --> {!}Terminal [!=,==] {!}Terminal | {!}Terminal | {!}(Expression)
Terminal --> Number or Variable
Usage:
from boolparser import *
p = BooleanParser('<expression text>')
p.evaluate(variable_dict) # variable_dict is a dictionary providing values for variables that appear in <expression text>
"""


class TreeNode:
    def __init__(self, token_type):
        self.left = None
        self.right = None
        self.value = None
        self.tokenType = token_type
        self.negate = False
        self.carryover = []


class BooleanParser:
    def __init__(self, exp):
        self.root = None
        self.tokenizer = Tokenizer(exp)
        self.tokenizer.tokenize()
        self.parse()

    def parse(self):
        whole_expression_negated = False

        if self.tokenizer.nextTokenType() == self.tokenizer.getToken('not'):
            whole_expression_negated = True
            self.tokenizer.next()

            # additional check, first token negates only variable, not the whole formula
            if self.tokenizer.nextTokenType() != self.tokenizer.getToken('lp'):
                whole_expression_negated = False

        self.root = self.parseExpression()
        if whole_expression_negated:
            self.root.negate = True
            self.root.carryover.append[self.tokenizer.getToken('not')]

    def parseExpression(self):
        andTerm1 = self.parseAndTerm()

        or_token_type = self.tokenizer.getToken('or')
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == or_token_type:
            self.tokenizer.next()
            andTermX = self.parseAndTerm()
            andTerm = TreeNode(or_token_type)
            andTerm.left = andTerm1
            andTerm.right = andTermX
            andTerm1 = andTerm
        return andTerm1

    def parseAndTerm(self):
        condition1 = self.parseCondition()

        and_token_type = self.tokenizer.getToken('and')
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == and_token_type:
            self.tokenizer.next()
            conditionX = self.parseCondition()
            condition = TreeNode(and_token_type)
            condition.left = condition1
            condition.right = conditionX
            condition1 = condition
        return condition1

    def parseCondition(self):
        negation_queued = False
        if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == self.tokenizer.getToken('not'):
            negation_queued = True
            self.tokenizer.next()
        if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == self.tokenizer.getToken('lp'):
            self.tokenizer.next()
            expression = self.parseExpression()
            if negation_queued:
                expression.negate = True
                expression.carryover.append(self.tokenizer.getToken('not'))
                negation_queued = False
            expression.carryover.append(self.tokenizer.getToken('lp'))
            expression.carryover.append(self.tokenizer.getToken('rp'))
            if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == self.tokenizer.getToken('rp'):
                self.tokenizer.next()
                return expression
            else:
                raise Exception("Closing ) expected, but got " +
                                self.tokenizer.peek())

        terminal1 = self.parseTerminal()
        if negation_queued:
            terminal1.negate = True
            negation_queued = False
        if self.tokenizer.hasNext() and self.tokenizer.nextTokenTypeIsOperator():
            condition = TreeNode(self.tokenizer.nextTokenType())
            self.tokenizer.next()
            if self.tokenizer.nextTokenType() == self.tokenizer.getToken('not'):
                negation_queued = True
            terminal2 = self.parseTerminal()
            if negation_queued:
                terminal2.negate = True
                negation_queued = False
            condition.left = terminal1
            condition.right = terminal2
            return condition
        elif not self.tokenizer.hasNext() or self.tokenizer.nextTokenType() in [self.tokenizer.getToken('rp'), self.tokenizer.getToken('and'), self.tokenizer.getToken('or')]:
            return terminal1
        else:
            raise Exception('Operator expected, but got ' +
                            self.tokenizer.next())

    def parseTerminal(self):
        if self.tokenizer.hasNext():
            tokenType = self.tokenizer.nextTokenType()
            if tokenType == self.tokenizer.getToken('val'):
                n = TreeNode(tokenType)
                n.value = bool(self.tokenizer.next())
                return n
            elif tokenType == self.tokenizer.getToken('var'):
                n = TreeNode(tokenType)
                n.value = self.tokenizer.next()
                return n
            else:
                raise Exception(
                    'NUM or VAR expected, but got ' + self.tokenizer.next())

        else:
            raise Exception('NUM or VAR expected, but got ' +
                            self.tokenizer.next())

    def evaluate(self, variable_dict):
        return self.evaluateRecursive(self.root, variable_dict)

    def evaluateRecursive(self, treeNode, variable_dict):
        result = None
        if treeNode.tokenType == self.tokenizer.getToken('val'):
            result = treeNode.value
        elif treeNode.tokenType == self.tokenizer.getToken('var'):
            result = variable_dict.get(treeNode.value)

        if result != None:
            if treeNode.negate == True:
                return not result
            return result

        left = self.evaluateRecursive(treeNode.left, variable_dict)
        right = self.evaluateRecursive(treeNode.right, variable_dict)
        if treeNode.tokenType == self.tokenizer.getToken('eq'):
            result = left == right
        elif treeNode.tokenType == self.tokenizer.getToken('neq'):
            result = left != right
        elif treeNode.tokenType == self.tokenizer.getToken('and'):
            result = left and right
        elif treeNode.tokenType == self.tokenizer.getToken('or'):
            result = left or right
        else:
            raise Exception('Unexpected type ' + str(treeNode.tokenType))

        if treeNode.negate == True:
            return not result
        return result

    def toString(self):
        return self.toStringRecursive(self.root)

    def toStringRecursive(self, treeNode):
        current = ''
        left = ''
        right = ''

        treeNode = self.carryOver(treeNode)

        if treeNode.left != None:
            left = self.toStringRecursive(treeNode.left)
        else:
            for token in treeNode.carryover:
                if token == self.tokenizer.getToken('lp'):
                    left = left + '('
                elif token == self.tokenizer.getToken('not'):
                    left = left + '!'

        if treeNode.right != None:
            right = self.toStringRecursive(treeNode.right)
        else:
            for token in treeNode.carryover:
                if token == self.tokenizer.getToken('rp'):
                    right = ')' + right

        if treeNode.tokenType == self.tokenizer.getToken('val'):
            if treeNode.negate:
                current = not treeNode.value
            else:
                current = treeNode.value
        if treeNode.tokenType == self.tokenizer.getToken('var'):
            current = treeNode.value
            if treeNode.negate:
                current = '!' + current
        elif treeNode.tokenType == self.tokenizer.getToken('eq'):
            current = '=='
        elif treeNode.tokenType == self.tokenizer.getToken('neq'):
            current = '!='
        elif treeNode.tokenType == self.tokenizer.getToken('and'):
            current = ' and '
        elif treeNode.tokenType == self.tokenizer.getToken('or'):
            current = ' or '

        return left + current + right

    def carryOver(self, treeNode):
        for token in treeNode.carryover:
            if token == self.tokenizer.getToken('rp'):
                if treeNode.right != None:
                    treeNode.right.carryover.append(token)
            else:
                if treeNode.left != None:
                    treeNode.left.carryover.append(token)
        return treeNode

    # diagnostic
    def printTree(self, treeNode):
        print(treeNode.value, ", ", treeNode.tokenType, ": ", treeNode.carryover)

        if treeNode.left != None:
            print("GO LEFT")
            self.printTree(treeNode.left)
        if treeNode.right != None:
            print("GO RIGHT")
            self.printTree(treeNode.right)
