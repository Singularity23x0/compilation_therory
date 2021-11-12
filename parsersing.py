import ply.yacc as yacc
from lexer import *

precedence = (
    ('nonassoc', 'RANGE'),
    ('nonassoc', 'IFN'),
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', '+', '-', 'MTX_SUM', 'MTX_DIFFERENCE','ART'),
    ('left', '*', '/', 'MTX_PRODUCT', 'MTX_QUOTIENT'),
    ('right', 'UMINUS'),
    ('left', 'TRANSPOSE'),
)


def p_program(p):
    """program : segment
    | """


def p_segment(p):
    """segment : group segment
    | group"""


def p_line(p):
    """line : expression ';'
    | ';' """


def p_block(p):
    """block : '{' segment '}'"""


def p_for(p):
    """for : FOR ID '=' range group """


def p_range(p):
    """range : value_element ':' value_element %prec RANGE"""


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""


def p_if(p):
    """if : IF '(' logical_expression ')' group %prec IFN
    | IF '(' logical_expression ')' group ELSE group %prec IFX"""


def p_group(p):
    """group : conditional
    | line
    | block"""


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
    | matrix_definition
    | select_element"""


def p_select_element(p):
    """ select_element : value_element matrix_row"""


def p_matrix_definition(p):
    """matrix_definition : '[' matrix_definition_inside ']'
     | matrix_gen_func """


def p_matrix_definition_inside(p):
    """matrix_definition_inside : matrix_row ',' matrix_definition_inside
    | matrix_row """


def p_matrix_row(p):
    """ matrix_row : '[' vector ']' """


def p_vector(p):
    """ vector : value_element ',' vector
    | value_element"""


def p_matrix_gen_func(p):
    """ matrix_gen_func : func_name '(' value_element ')' """


def p_func_name(p):
    """ func_name : EYE
    | ONES
    | ZEROS """


def p_arithmetic_expression(p):
    """arithmetic_expression : value_element arithmetic_operator value_element %prec ART
    | '(' value_element ')' """


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
    | value_element
    | BREAK
    | CONT
    | return
    | print """


def p_logical_expression(p):
    """logical_expression : value_element comparison_operator value_element"""


def p_comparison_operator(p):
    """comparison_operator : '<'
    | '>'
    | EQUAL
    | NOT_EQUAL
    | SMALLER_OR_EQUAL
    | LARGER_OR_EQUAL"""


def p_assignment_operator(p):
    """assignment_operator : '='
    | ADD
    | SUBTRACT
    | MULTIPLY
    | DIVIDE """


def p_assignment(p):
    """assignment : ID assignment_operator value_element
    | select_element assignment_operator value_element
    | select_element assignment_operator matrix_row"""


def p_print(p):
    """ print : PRINT vector"""


def p_return(p):
    """ return : RETURN value_element
    | RETURN """


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parserA = yacc.yacc()



