class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"Number({self.token.value})"

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op.value}, {self.right})"

class UnaryOpNode(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f"UnaryOp({self.op.value}, {self.expr})"

class VariableNode(ASTNode):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"Variable({self.token.value})"

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        return self.statement()

    def statement(self):
        if self.current_token.type == "IDENTIFIER" and self.peek().type == "OPERATOR" and self.peek().value == "=":
            return self.assignment()
        return self.expr()

    def assignment(self):
        name = self.current_token
        self.advance()  # Consume identifier
        self.advance()  # Consume '='
        value = self.expr()
        return AssignmentNode(name.value, value)

    def expr(self):
        node = self.term()

        while self.current_token and self.current_token.type == "OPERATOR" and self.current_token.value in ("+", "-"):
            op = self.current_token
            self.advance()
            right = self.term()
            node = BinaryOpNode(node, op, right)

        return node

    def term(self):
        node = self.factor()

        while self.current_token and self.current_token.type == "OPERATOR" and self.current_token.value in ("*", "/"):
            op = self.current_token
            self.advance()
            right = self.factor()
            node = BinaryOpNode(node, op, right)

        return node

    def factor(self):
        token = self.current_token

        if token.type == "INTEGER" or token.type == "FLOAT":
            self.advance()
            return NumberNode(token)
        elif token.type == "IDENTIFIER":
            self.advance()
            return VariableNode(token)
        elif token.type == "OPERATOR" and token.value in ("+", "-"):
            self.advance()
            factor = self.factor()
            return UnaryOpNode(token, factor)
        elif token.type == "PUNCTUATION" and token.value == "(":
            self.advance()
            expr = self.expr()
            if self.current_token.type == "PUNCTUATION" and self.current_token.value == ")":
                self.advance()
                return expr
            else:
                raise SyntaxError("Expected closing parenthesis")
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def peek(self):
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1]
        return None
