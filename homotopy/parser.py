import ply.lex as lex
import ply.yacc as yacc
from homotopy.syntax_tree import SimpleSnippet, CompositeSnippet

# Lexer

# List of token names.
tokens = (
    'SNIPPET',
    'LEFT_OPERATOR',
    'RIGHT_OPERATOR',
)

# Starting letters of operators.
left = '!@#'
right = '$%:'

# Regular expression rules for tokens
t_SNIPPET = r'[a-zA-Z_0-9]+'
t_LEFT_OPERATOR = r'[{0}][{0}{1}]*'.format(left, right)
t_RIGHT_OPERATOR = r'[{1}][{0}{1}]*'.format(left, right)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parser

# Set up precedence.
precedence = (
    ('left', 'LEFT_OPERATOR'),
    ('right', 'RIGHT_OPERATOR'),
)


# Grammar rules.
def p_expression_plus(p):
    """
    expression : expression LEFT_OPERATOR expression
               | expression RIGHT_OPERATOR expression
    """
    p[0] = CompositeSnippet(p[1], p[2], p[3])


def p_expression_minus(p):
    """
    expression : SNIPPET 
    """
    p[0] = SimpleSnippet(p[1])


# Build the parser
parser = yacc.yacc()
