import re
import sys

# Lexer Code
class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, Line: {self.line}, Column: {self.column})"

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_line = 1
        self.current_column = 1

        # Define token patterns using regex
        self.token_patterns = [
            (r'\n', "NEWLINE"),
            (r'\s+', "WHITESPACE"),
            (r'\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b', "KEYWORD"),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', "IDENTIFIER"),
            (r'\b\d+\b', "INTEGER"),
            (r'\b\d+\.\d+\b', "FLOAT"),
            (r'"[^"]*"', "STRING"),
            (r'\+|\-|\*|\/|\==|\!=|\>|<|\&\&|\|\||=', "OPERATOR"),
            (r'[;,()\[\]{}:]', "PUNCTUATION"),
            (r'#.*', "COMMENT"),
        ]

        # Compile regex patterns for efficiency
        self.token_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for pattern, name in self.token_patterns if name))

    def tokenize(self):
        position = 0
        while position < len(self.source_code):
            match = self.token_regex.match(self.source_code, position)
            if not match:
                sys.stderr.write(
                    f"Illegal character at Line {self.current_line}, Column {self.current_column}: {repr(self.source_code[position])}\n")
                sys.exit(1)

            token_type = match.lastgroup
            token_value = match.group(token_type)

            # Properly update line and column numbers
            if token_type == "NEWLINE":
                self.current_line += 1
                self.current_column = 1
            elif token_type == "WHITESPACE":
                self.current_column += len(token_value)
            elif token_type == "COMMENT":
                self.current_column += len(token_value)
            else:
                self.tokens.append(Token(token_type, token_value, self.current_line, self.current_column))
                self.current_column += len(token_value)

            # Move to the next position
            position = match.end()

        return self.tokens


# Parser Code
class ASTNode:
    pass

class FunctionDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name}, Params: {self.params}, Body: {self.body})"

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"

class CallNode(ASTNode):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f"Call({self.func_name}, Args: {self.args})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = -1
        self.advance()

    def advance(self):
        """Advances to the next token."""
        if self.current_token_index + 1 < len(self.tokens):
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def parse(self):
        """Parse the tokens into an AST."""
        nodes = []
        
        while self.current_token is not None:
            if self.current_token.type == "KEYWORD" and self.current_token.value == "def":
                nodes.append(self.function_def())
            else:
                # Skip unrecognized statements for simplicity; can be expanded later.
                print(f"Skipping unrecognized token: {self.current_token}")
                self.advance()

        return nodes

    def function_def(self):
        """Parse a function definition."""
        self.advance()  # Consume 'def'
        
        if not (self.current_token.type == "IDENTIFIER"):
            raise SyntaxError("Expected function name")
        
        func_name = self.current_token.value
        self.advance()  # Consume function name
        
        if not (self.current_token.type == "PUNCTUATION" and self.current_token.value == "("):
            raise SyntaxError("Expected '(' after function name")
        
        params = []
        
        # Parse parameters within parentheses
        while True:
            self.advance()  # Consume '(' or parameter
            
            if self.current_token.type == "IDENTIFIER":
                params.append(self.current_token.value)
                self.advance()  # Consume parameter
            
                if not (self.current_token.type in ("PUNCTUATION", "NEWLINE") and 
                        (self.current_token.value == "," or 
                         (self.current_token.value == ")" and len(params) > 0))):
                    raise SyntaxError("Expected ',' or ')' in parameter list")

                if self.current_token.value == ")":
                    break
            
            elif self.current_token.type == "PUNCTUATION" and \
                 (self.current_token.value == ")"):
                break
            
            else:
                raise SyntaxError("Invalid parameter list")

        
        body = []
        
        # Parse function body; assume single return statement for simplicity.
        while True:
            if not (self.current_token.type == "KEYWORD" and 
                    self.current_token.value == "return"):
                break
            
            body.append(self.return_stmt())
        
        return FunctionDefNode(func_name, params, body)

    def return_stmt(self):
        """Parse a return statement."""
        self.advance()  # Consume 'return'
        
        if not (self.current_token.type in ("IDENTIFIER", "INTEGER")):
            raise SyntaxError("Expected expression after 'return'")
        
        value = CallNode(self.current_token.value, [])
        
        # Advance to consume the expression.
        if value.func_name != 'return':
          raise SyntaxError("Invalid return statement")
          
          # Advance to consume expression.
          return ReturnNode(value)

