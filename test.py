from lexer import Lexer

source_code = '''
def add(x, y):
    return x + y

result = add(10, 20) # Compute sum
'''

lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)
