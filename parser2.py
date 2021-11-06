import ply.yacc as yacc
from lexer import *

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('left', 'MTX_SUM', 'MTX_DIFFERENCE'),
    ('left', 'MTX_PRODUCT', 'MTX_QUOTIENT'),
    ('right', 'TRANS')
)


def p_program(p):
    """program : segment
    | """


def p_segment(p):
    """segment : segment segment
    | group"""


def p_line(p):
    """line : expression ';'"""


def p_block(p):
    """block : '{' segment '}'"""


def p_for(p):
    """for : FOR ID '=' range group"""


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""


def p_if(p):
    """if : IF '(' logical_expression ')' group
    | IF '(' logical_expression ')' group ELSE group %prec IFX"""


def p_group(p):
    """group : conditional
    | line
    | block"""


def p_conditional(p):
    """conditional : if
    | while
    | for"""


def p_element(p):
    """element : ID
    | arithmetic_expression
    | FLOAT
    | INT
    | STRING
    | '-' element %prec UMINUS
    | element TRANSPOSE %prec TRANS"""
    # TODO add defined matrix


def p_expression(p):
    """expression : logical_expression
        | assignment
        | element"""


def p_logical_expression(p):
    """logical_expression : element comparison_operator element"""


def p_comparison_operator(p):
    """comparison_operator : '<'
    | '>'
    | EQUAL
    | NOT_EQUAL
    | SMALLER_OR_EQUAL
    | LARGER_OR_EQUAL"""


def p_arithmetic_expression(p):
    """arithmetic_expression : element arithmetic_operator element"""


def p_arithmetic_operator(p):
    """ arithmetic_operator : '+'
    | '-'
    | '*'
    | '/'
    | MTX_SUM
    | MTX_DIFFERENCE
    | MTX_PRODUCT
    | MTX_QUOTIENT """


# def p_matrix(p):
#     """matrix :"""
#     #| matrix_function
#     #| matrix_literal

def p_range(p):
    """range : element ':' element"""


def p_assignment(p):
    """assignment : ID '=' element"""


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parserA = yacc.yacc()



