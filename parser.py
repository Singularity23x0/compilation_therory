import ply.yacc as yacc
from lexer import *


precedence = (
    ('nonasoc', 'IFX'),
    ('nonasco', 'ELSE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('left', 'MTX_SUM', 'MTX_DIFFERENCE'),
    ('left', 'MTX_PRODUCT', 'MTX_QUOTIENT'),
    ('right', 'MUMINUS'),
    ('right', 'TRANS')
)


def p_program(p):
    """program : segment"""


def p_segment(p):
    """segment
    : segment segment
    | group
    | empty"""


def p_line(p):
    """line : expression ';'"""


def p_block(p):
    """block : '{' segment '}'"""


def p_for(p):
    """for : FOR ID '=' range group"""


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""


def p_if(p):
    """if
    : IF '(' logical_expression ')' group
    | IF '(' logical_expression ')' group ELSE group %prec IFX"""


def p_group(p):
    """group
    : conditional
    | line
    | block"""


def p_conditional(p):
    """conditional
    : if
    | while
    | for"""


def p_expression(p):
    """expression
    : logical_expression
    | assignment
    | arithmetic_expression
    | matrix_expression
    | string_expression"""


def p_logical_expression(p):
    """logical_expression
    : arithmetic_expression comparison_operator arithmetic_expression
    | matrix_expression EQUAL matrix_expression
    | matrix_expression NOT_EQUAL matrix_expression
    | string_expression comparison_operator string_expression"""


def p_comparison_operator(p):
    """comparison_operator
    : '<'
    | '>'
    | EQUAL
    | NOT_EQUAL
    | SMALLER_OR_EQUAL
    | LARGER_OR_EQUAL"""


def p_number(p):
    """number
    : - number %prec UMINUS
    | INT
    | FLOAT
    | ID
    | arithmetic_expression """


def p_arithmetic_expression(p):
    """arithmetic_expression
    : number
    | number arithmetic_operator number"""


def p_arithmetic_operator(p):
    """arithmetic_operator
    : +
    | -
    | *
    | /"""


def p_matrix(p):
    """matrix
    : - matrix %prec MUMINUS
    | matrix '\'' %prec TRANS
    | ID
    | matrix_function
    | matrix_literal
    | matrix_expression """


def p_matrix_expression(p):
    """matrix_expression
    : matrix
    | matrix matrix_operator matrix"""


def p_matrix_operator(p):
    """matrix_operator
    : MTX_SUM
    | MTX_DIFFERENCE
    | MTX_PRODUCT
    | MTX_QUOTIENT
    | '+'
    | '-'
    | '*' """


def p_string(p):
    """string
    : STRING
    | ID
    | string_expression """


def p_string_expression(p):
    """string_expression
    : string
    | string '+' string"""


def p_range(p):
    """range
    : number ':' number"""


def p_assignment(p):
    """assignment
    : ID '=' number
    | ID '=' matrix
    | ID '=' string
    | ID '=' ID """





