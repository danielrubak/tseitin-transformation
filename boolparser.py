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

# TODO: some of expression needs parenthesis on the beginning and the end, there is need to add additional validation
# TODO: TokenType should not be class, rather a field in BooleanParser or sth like that because there is no possibility to get type names

class TokenType:
	VAL, VAR, EQ, NEQ, LP, RP, AND, OR, NOT = range(9)

class TreeNode:
	tokenType = None
	value = None
	left = None
	right = None
	negate = None
	carryover = None

	def __init__(self, tokenType):
		self.tokenType = tokenType
		self.negate = False
		self.carryover = []

class Tokenizer:
	expression = None
	tokens = None
	tokenTypes = None
	i = 0
	
	def __init__(self, exp):
		self.expression = exp

	def next(self):
		self.i += 1
		return self.tokens[self.i-1]
	
	def peek(self):
		return self.tokens[self.i]
	
	def hasNext(self):
		return self.i < len(self.tokens)

	def nextTokenType(self):
		return self.tokenTypes[self.i]
	
	def nextTokenTypeIsOperator(self):
		t = self.tokenTypes[self.i]
		return t == TokenType.EQ or t == TokenType.NEQ

	def tokenize(self):
		import re
		reg = re.compile(r'(\bTrue\b|\bFalse\b|\bAND\b|\band\b|&&|\bOR\b|\bor\b|\|\||\bNOT\b|\bnot\b|~|!|!=|==|\(|\))')
		
		# every symbol in the input expression should be separate element on list
		self.tokens = reg.split(self.expression)

		# remove '=' symbol from expression if it appears with '!'
		for idx in range(len(self.tokens)):
			if self.tokens[idx] == '!' and re.match('=.*', self.tokens[idx+1]):
				self.tokens[idx] = '!='
				self.tokens[idx+1] = self.tokens[idx+1][1:]

		# remove white characters
		self.tokens = [t.strip() for t in self.tokens if t.strip() != '']

		self.tokenTypes = []
		for t in self.tokens:
			if t == 'AND' or t == 'and' or t == '&&':
				self.tokenTypes.append(TokenType.AND)
			elif t == 'OR' or t == 'or' or t == '||':
				self.tokenTypes.append(TokenType.OR)
			elif t == 'NOT' or t == 'not' or t == '~' or t == '!':
				self.tokenTypes.append(TokenType.NOT)
			elif t == '(':
				self.tokenTypes.append(TokenType.LP)
			elif t == ')':
				self.tokenTypes.append(TokenType.RP)
			elif t == '==':
				self.tokenTypes.append(TokenType.EQ)
			elif t == '!=':
				self.tokenTypes.append(TokenType.NEQ)
			elif t == 'True' or t == 'False' or re.fullmatch('[0-1]',t):
				self.tokenTypes.append(TokenType.VAL)
			elif re.search('^[a-zA-Z_]+$', t):
				self.tokenTypes.append(TokenType.VAR)
			else:
				self.tokenTypes.append(None)


class BooleanParser:
	tokenizer = None
	root = None

	def __init__(self, exp):
		self.tokenizer = Tokenizer(exp)
		self.tokenizer.tokenize()
		self.parse()

	def parse(self):
		whole_expression_negated = False
		if self.tokenizer.nextTokenType() == TokenType.NOT:
			whole_expression_negated = True
			self.tokenizer.next()
		self.root = self.parseExpression()
		if whole_expression_negated:
			self.root.negate = True
			self.root.carryover.append[TokenType.NOT]

	def parseExpression(self):
		andTerm1 = self.parseAndTerm()
		while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenType.OR:
			self.tokenizer.next()
			andTermX = self.parseAndTerm()
			andTerm = TreeNode(TokenType.OR)
			andTerm.left = andTerm1
			andTerm.right = andTermX
			andTerm1 = andTerm
		return andTerm1

	def parseAndTerm(self):
		condition1 = self.parseCondition()
		while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenType.AND:
			self.tokenizer.next()
			conditionX = self.parseCondition()
			condition = TreeNode(TokenType.AND)
			condition.left = condition1
			condition.right = conditionX
			condition1 = condition
		return condition1

	def parseCondition(self):
		negation_queued = False
		if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenType.NOT:
			negation_queued = True
			self.tokenizer.next()
		if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenType.LP:
			self.tokenizer.next()
			expression = self.parseExpression()
			if negation_queued:
				expression.negate = True
				expression.carryover.append(TokenType.NOT)
				negation_queued = False
			expression.carryover.append(TokenType.LP)
			expression.carryover.append(TokenType.RP)
			if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == TokenType.RP:
				self.tokenizer.next()
				return expression
			else:
				raise Exception("Closing ) expected, but got " + self.tokenizer.next())

		terminal1 = self.parseTerminal()
		if negation_queued:
			terminal1.negate = True
			negation_queued = False
		if self.tokenizer.hasNext() and self.tokenizer.nextTokenTypeIsOperator():
			condition = TreeNode(self.tokenizer.nextTokenType())
			self.tokenizer.next()
			if self.tokenizer.nextTokenType() == TokenType.NOT:
				negation_queued = True
			terminal2 = self.parseTerminal()
			if negation_queued:
				terminal2.negate = True
				negation_queued = False
			condition.left = terminal1
			condition.right = terminal2
			return condition
		elif self.tokenizer.hasNext() and self.tokenizer.nextTokenType() in [TokenType.RP, TokenType.AND, TokenType.OR]:
			return terminal1
		else:
			raise Exception('Operator expected, but got ' + self.tokenizer.next())
	
	def parseTerminal(self):
		if self.tokenizer.hasNext():
			tokenType = self.tokenizer.nextTokenType()
			if tokenType == TokenType.VAL:
				n = TreeNode(tokenType)
				n.value = bool(self.tokenizer.next())
				return n
			elif tokenType == TokenType.VAR:
				n = TreeNode(tokenType)
				n.value = self.tokenizer.next()
				return n
			else:
				raise Exception('NUM or VAR expected, but got ' + self.tokenizer.next())
		
		else:
			raise Exception('NUM or VAR expected, but got ' + self.tokenizer.next())
	
	def evaluate(self, variable_dict):
		return self.evaluateRecursive(self.root, variable_dict)
	
	def evaluateRecursive(self, treeNode, variable_dict):
		result = None
		if treeNode.tokenType == TokenType.VAL:
			result = treeNode.value
		elif treeNode.tokenType == TokenType.VAR:
			result = variable_dict.get(treeNode.value)
		
		if result != None:
			if treeNode.negate == True:
				return not result
			return result
		
		left = self.evaluateRecursive(treeNode.left, variable_dict)
		right = self.evaluateRecursive(treeNode.right, variable_dict)
		if treeNode.tokenType == TokenType.EQ:
			result = left == right
		elif treeNode.tokenType == TokenType.NEQ:
			result = left != right
		elif treeNode.tokenType == TokenType.AND:
			result = left and right
		elif treeNode.tokenType == TokenType.OR:
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
				if token == TokenType.LP:
					left = left + '('
				elif token == TokenType.NOT:
					left = left + '!'


		if treeNode.right != None:
			right = self.toStringRecursive(treeNode.right)
		else:
			for token in treeNode.carryover:
				if token == TokenType.RP:
					right = ')' + right

		if treeNode.tokenType == TokenType.VAL:
			if treeNode.negate:
				current = not treeNode.value
			else:
				current = treeNode.value
		if treeNode.tokenType == TokenType.VAR:
			current = treeNode.value
			if treeNode.negate:
				current = '!' + current
		elif treeNode.tokenType == TokenType.EQ:
			current = '=='
		elif treeNode.tokenType == TokenType.NEQ:
			current = '!='
		elif treeNode.tokenType == TokenType.AND:
			current = ' and '
		elif treeNode.tokenType == TokenType.OR:
			current = ' or '

		return left + current + right

	def carryOver(self, treeNode):
		for token in treeNode.carryover:
			if token == TokenType.RP:
				if treeNode.right != None:
					treeNode.right.carryover.append(token)
			else:
				if treeNode.left != None:
					treeNode.left.carryover.append(token)
		return treeNode

	#diagnostic
	def printTree(self, treeNode):
		tokenMap = { 0: "VAL", 1: "VAR", 2: "EQ", 3: "NEQ", 4: "LP", 
					5: "RP", 6: "AND", 7: "OR", 8: "NOT"}

		print(tokenMap[treeNode.tokenType], ": ", 
		[tokenMap[co] for co in treeNode.carryover])
		
		print("check left")
		if treeNode.left != None:
			print("left exists")
			self.printTree(treeNode.left)
		print("check right")
		if treeNode.right != None:
			print("right exists")
			self.printTree(treeNode.right)
