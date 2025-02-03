import re
import sys

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
            (r'\n', "NEWLINE"),  # Recognize newlines instead of treating them as illegal
            (r'\s+', "WHITESPACE"),  # Explicitly handle whitespace
            (r'\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b', "KEYWORD"),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', "IDENTIFIER"),
            (r'\b\d+\b', "INTEGER"),
            (r'\b\d+\.\d+\b', "FLOAT"),
            (r'"[^"]*"', "STRING"),
            (r'\+|\-|\*|\/|==|!=|>|<|&&|\|\||=', "OPERATOR"),  # Added '=' to the operator pattern
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
                self.current_column += len(token_value)  # Just skip whitespace
            elif token_type == "COMMENT":
                self.current_column += len(token_value)  # Ignore comments, but update position
            else:
                self.tokens.append(Token(token_type, token_value, self.current_line, self.current_column))
                self.current_column += len(token_value)

            # Move to the next position
            position = match.end()

        return self.tokens
