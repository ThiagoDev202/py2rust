from pyparsing import *

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
