from pyparsing import *
from transpiler_ast import ProgramNode, ExpressionNode, AssignmentNode, PrintNode, IfNode, FunctionNode

# Define parser elements for basic components
integer = pyparsing_common.signed_integer
identifier = Word(alphas, alphanums + "_")
stringLiteral = QuotedString('"')

# Define an expression parser with operator precedence
expr = infixNotation(integer | identifier | stringLiteral,
                     [
                         (oneOf("* /"), 2, opAssoc.LEFT),
                         (oneOf("+ -"), 2, opAssoc.LEFT),
                         (oneOf("== != < > <= >="), 2, opAssoc.LEFT),
                     ])

# Statements
assignment = identifier + "=" + expr + ";"
printStatement = "print(" + expr + ");"

# Define blocks for if statements and functions
if_expr = "if" + expr + ":"
if_block = Group(if_expr + IndentedBlock(assignment | printStatement))

function_def = "def" + identifier + "(" + Optional(delimitedList(identifier)) + "):"
function_block = Group(function_def + IndentedBlock(assignment | printStatement | if_block))

# Program structure to allow multiple statements
program = ZeroOrMore(if_block | function_block | assignment | printStatement)

# Adjusting the grammar to avoid strict end of text requirement
parser = program.ignore(White())

# Crie funções para converter tokens em nós da AST
def parse_assignment(tokens):
    # Garanta que tokens[2] é uma lista ou converta adequadamente
    expression = " ".join(str(x) for x in tokens[2]) if isinstance(tokens[2], (list, ParseResults)) else str(tokens[2])
    return AssignmentNode(tokens[0], ExpressionNode(expression))

def parse_print(tokens):
    # Similar ao acima, garantindo que tokens[1] seja tratado corretamente
    expression = " ".join(str(x) for x in tokens[1]) if isinstance(tokens[1], (list, ParseResults)) else str(tokens[1])
    return PrintNode(ExpressionNode(expression))

def parse_if(tokens):
    condition = ExpressionNode(" ".join(str(x) for x in tokens[1]))
    if_node = IfNode(condition)
    true_block = tokens[2]  # Este é o bloco de tokens verdadeiros
    if isinstance(true_block, (list, ParseResults)):
        for stmt in true_block:
            if_node.add_if_statement(parse_statement(stmt))
    # Implemente lógica para 'else' se necessário
    return if_node

def parse_function(tokens):
    name = tokens[1]
    params = [ExpressionNode(p) for p in tokens[2]] if len(tokens) > 2 else []
    body = []
    body_tokens = tokens[3]  # Este é o bloco de tokens do corpo da função
    if isinstance(body_tokens, (list, ParseResults)):
        for stmt in body_tokens:
            body.append(parse_statement(stmt))
    function_node = FunctionNode(name, params)
    for stmt in body:
        function_node.add_to_body(stmt)
    return function_node

def parse_statement(stmt):
    # Certifique-se de que a estrutura de stmt esteja corretamente avaliada
    if isinstance(stmt, ParseResults):
        if stmt[0] == "if":
            condition = ExpressionNode(" ".join(map(str, stmt[1])))
            if_node = IfNode(condition)
            # Presumindo que stmt[2] seja o bloco verdadeiro (corpo do if)
            for sub_stmt in stmt[2]:
                if_node.add_if_statement(parse_statement(sub_stmt))
            return if_node
        elif stmt[0] == "=" and len(stmt) == 3:
            return parse_assignment(stmt)
        elif stmt[0].startswith("print"):
            return parse_print(stmt)
        elif stmt[0] == "def":
            name = stmt[1]
            params = [ExpressionNode(p) for p in stmt[2]] if len(stmt) > 2 else []
            body = []
            for sub_stmt in stmt[3]:
                body.append(parse_statement(sub_stmt))
            function_node = FunctionNode(name, params)
            for sub_stmt in body:
                function_node.add_to_body(sub_stmt)
            return function_node
        else:
            raise ValueError(f"Unrecognized statement type: {stmt}")
    else:
        # Lidar com expressões simples como atribuições fora dos blocos
        return parse_assignment(stmt)

# Adicione ações de parse aos seus elementos de parser
assignment.setParseAction(lambda tokens: parse_assignment(tokens))
printStatement.setParseAction(lambda tokens: parse_print(tokens))

# Exemplo simples de parsing e construção da AST
def build_ast(parsed_code):
    program_node = ProgramNode()
    for element in parsed_code:
        # Transforma o resultado do parser em nós AST antes de adicionar ao programa
        node = parse_statement(element)
        program_node.add_child(node)
    return program_node  # Construa a AST

# Use um container AST para manter todos os nós
program_node = ProgramNode()

# Test the parser
test_code = """
x = 10;
if x < 20:
    print(x);
    if x < 15:
        x = 5;
def func():
    y = 30;
    print(y);
"""

# Parse the test code
try:
    parsed_code = parser.parseString(test_code)
    print("Parsed successfully:")
    for item in parsed_code:
        print(item)
except ParseException as pe:
    print("Error in parsing:", str(pe))


