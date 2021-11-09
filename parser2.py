import ply.yacc as yacc
from lexer import *

precedence = (
    #('nonassoc', 'EQUAL','NOT_EQUAL','SMALLER_OR_EQUAL','LARGER_OR_EQUAL'),
    #('nonassoc', '='),
    #('nonassoc', 'ARITH_EXP'),
    #('nonassoc', 'FLOAT'),
    #('nonassoc', 'INT'),
    #('nonassoc', 'STRING'),
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'MTX_SUM', 'MTX_DIFFERENCE'),
    ('left', 'MTX_PRODUCT', 'MTX_QUOTIENT'),
    ('right', 'UMINUS'),
    ('right', 'TRANSPOSE')
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
    """for : FOR ID '=' range group """


def p_range(p):
    """range : value_element ':' value_element"""


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""


def p_if(p):
    """if : IF '(' logical_expression ')' group
    | IF '(' logical_expression ')' group ELSE group %prec IFX"""


def p_group(p):
    """group : conditional
    | line
    | block """


def p_conditional(p):
    """conditional : if
    | while
    | for"""


def p_value_element(p):
    """value_element : ID
    | arithmetic_expression
    | FLOAT
    | INT
    | STRING
    | '-' value_element %prec UMINUS
    | value_element TRANSPOSE
    | matrix_definition"""


def p_matrix_definition(p):
    """matrix_definition : '[' matrix_definition_inside ']'"""


def p_matrix_definition_inside(p):
    """matrix_definition_inside : matrix_definition_inside matrix_definition_inside
    | value_element ','"""


def p_arithmetic_expression(p):
    """arithmetic_expression : value_element arithmetic_operator value_element"""


def p_arithmetic_operator(p):
    """ arithmetic_operator : '+'
    | '-'
    | '*'
    | '/'
    | MTX_SUM
    | MTX_DIFFERENCE
    | MTX_PRODUCT
    | MTX_QUOTIENT """


def p_expression(p):
    """expression : logical_expression
        | assignment
        | value_element"""


def p_logical_expression(p):
    """logical_expression : value_element comparison_operator value_element"""


def p_comparison_operator(p):
    """comparison_operator : '<'
    | '>'
    | EQUAL
    | NOT_EQUAL
    | SMALLER_OR_EQUAL
    | LARGER_OR_EQUAL"""


def p_assignment(p):
    """assignment : ID '=' value_element"""


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parserA = yacc.yacc()



