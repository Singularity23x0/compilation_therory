import ply.yacc as yacc
from lexer import *


precedence = (
    ('nonasoc', 'IFX'),
    ('nonasco', 'ELSE')
)


def p_program(p):
    """program : segment"""


def p_segment(p):
    """segment
    : segment segment
    | group"""


def p_line(p):
    """line : expression ;"""


def p_block(p):
    """block : { segment }"""


def p_for(p):
    """for : FOR ID = range group"""


def p_while(p):
    """while : WHILE ( logical_expression ) group"""


def p_if(p):
    """if
    : IF ( logical_expression ) group
    | IF ( logical_expression ) group ELSE group %prec IFX"""


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
    | arithmetic_expression"""


def p_logical_expression(p):
    """logical_expression
    : arithmetic_expression comparison_operator arithmetic_expression
    | matrix_expression EQUAL matrix_expression
    | matrix_expression NOT_EQUAL matrix_expression"""


def p_comparison_operator(p):
    """comparison_operator
    : <
    | >
    | EQUAL
    | NOT_EQUAL
    | SMALLER_OR_EQUAL
    | LARGER_OR_EQUAL"""


def p_arithmetic_expression(p):
    """arithmetic_expression
    : INT
    | FLOAT
    | ID
    | arithmetic_expression """

