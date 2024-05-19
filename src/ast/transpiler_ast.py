class ASTNode:
    """Base class for all AST nodes."""
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __repr__(self):
        return self.name + "(" + ', '.join(repr(child) for child in self.children) + ")"

class ProgramNode(ASTNode):
    """Represents the entire program."""
    def __init__(self):
        super().__init__("Program")

class ExpressionNode(ASTNode):
    """Represents an expression."""
    def __init__(self, expression):
        super().__init__("Expression")
        self.expression = expression

class AssignmentNode(ASTNode):
    """Represents an assignment statement."""
    def __init__(self, identifier, expression):
        super().__init__("Assignment")
        self.identifier = identifier
        self.expression = expression

class PrintNode(ASTNode):
    """Represents a print statement."""
    def __init__(self, expression):
        super().__init__("Print")
        self.expression = expression

class IfNode(ASTNode):
    """Represents an if statement."""
    def __init__(self, condition):
        super().__init__("If")
        self.condition = condition
        self.if_body = []
        self.else_body = []

    def add_if_statement(self, statement):
        self.if_body.append(statement)
        statement.parent = self

    def add_else_statement(self, statement):
        self.else_body.append(statement)
        statement.parent = self

class FunctionNode(ASTNode):
    """Represents a function definition."""
    def __init__(self, name, parameters):
        super().__init__("Function")
        self.name = name
        self.parameters = parameters
        self.body = []

    def add_to_body(self, statement):
        self.body.append(statement)
        statement.parent = self
