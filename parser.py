class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
        else:
            raise SyntaxError(f"Unexpected token {self.current_token}, expected {token_type}")

    def parse(self):
        statements = []
        while self.current_token:
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token.type == "IDENTIFIER":
            return self.assignment()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token}")

    def assignment(self):
        identifier = self.current_token
        self.eat("IDENTIFIER")
        self.eat("OPERATOR")  # Expect '='
        expr = self.expression()
        return ("ASSIGNMENT", identifier, expr)

    def expression(self):
        node = self.term()
        while self.current_token and self.current_token.type == "OPERATOR" and self.current_token.value in ('+', '-'):
            operator = self.current_token
            self.eat("OPERATOR")
            right = self.term()
            node = ("BINARY_OP", operator, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.current_token and self.current_token.type == "OPERATOR" and self.current_token.value in ('*', '/'):
            operator = self.current_token
            self.eat("OPERATOR")
            right = self.factor()
            node = ("BINARY_OP", operator, node, right)
        return node

    def factor(self):
        token = self.current_token
        if token.type == "INTEGER":
            self.eat("INTEGER")
            return ("INTEGER", token)
        elif token.type == "FLOAT":
            self.eat("FLOAT")
            return ("FLOAT", token)
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return ("VARIABLE", token)
        elif token.type == "PUNCTUATION" and token.value == '(':
            self.eat("PUNCTUATION")
            expr = self.expression()
            self.eat("PUNCTUATION")  # Expect ')'
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token}")
