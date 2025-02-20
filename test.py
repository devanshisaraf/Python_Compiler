from lexer import Lexer
from parser import Parser
# Test Code
source_code = '''
def add(x, y):
    return x + y

result = add(10, 20) # Compute sum
'''

lexer = Lexer(source_code)
tokens = lexer.tokenize()

print("Tokens:")
for token in tokens:
    print(token)

parser = Parser(tokens)
ast_nodes = parser.parse()

print("\nAST Nodes:")
for node in ast_nodes:
    print(node)
