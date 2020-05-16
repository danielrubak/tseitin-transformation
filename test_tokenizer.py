import unittest
from Tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):
    def test_tokenize_1 (self):
        tokenizer = Tokenizer('(a || b) && c || !(d && e)')
        tokenizer.tokenize()

        tokens_result = ['(', 'a', '||', 'b', ')', '&&', 'c', '||', '!', '(', 'd', '&&', 'e', ')']
        token_types_result = ['LP','VAR','OR','VAR','RP','AND','VAR','OR','NOT','LP','VAR','AND','VAR','RP']

        self.assertEqual(tokenizer.tokens, tokens_result)
        self.assertEqual(tokenizer.tokenTypes, token_types_result)

    def test_tokenize_2 (self):
        tokenizer = Tokenizer('(!(p && (q || !r)))')
        tokenizer.tokenize()

        tokens_result = ['(', '!', '(', 'p', '&&', '(', 'q', '||', '!', 'r', ')', ')', ')']
        token_types_result = ['LP','NOT','LP','VAR','AND','LP','VAR','OR','NOT','VAR','RP','RP','RP']

        self.assertEqual(tokenizer.tokens, tokens_result)
        self.assertEqual(tokenizer.tokenTypes, token_types_result)

    def test_tokenize_3 (self):
        tokenizer = Tokenizer('(a && b) || (a && !c)')
        tokenizer.tokenize()

        tokens_result = ['(', 'a', '&&', 'b', ')', '||', '(', 'a', '&&', '!', 'c', ')']
        token_types_result = ['LP', 'VAR', 'AND', 'VAR', 'RP', 'OR', 'LP', 'VAR', 'AND', 'NOT', 'VAR', 'RP']

        self.assertEqual(tokenizer.tokens, tokens_result)
        self.assertEqual(tokenizer.tokenTypes, token_types_result)

    def test_tokenize_4 (self):
        tokenizer = Tokenizer('(a && b) or ((c || d) and e)')
        tokenizer.tokenize()

        tokens_result = ['(', 'a', '&&', 'b', ')', 'or', '(', '(', 'c', '||', 'd', ')', 'and', 'e', ')']
        token_types_result = ['LP','VAR','AND','VAR','RP','OR','LP','LP','VAR','OR','VAR','RP','AND','VAR','RP']

        self.assertEqual(tokenizer.tokens, tokens_result)
        self.assertEqual(tokenizer.tokenTypes, token_types_result)

if __name__ == '__main__':
    unittest.main()