import ply.yacc as yacc
from lexer import *

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', '+', '-', 'MTX_SUM', 'MTX_DIFFERENCE'),
    ('left', '*', '/', 'MTX_PRODUCT', 'MTX_QUOTIENT'),
    ('right', 'UMINUS'),
    ('left', 'TRANSPOSE')
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
    """range : arithmetic_expression ':' arithmetic_expression """


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""


def p_if(p):
    """if : IF '(' logical_expression ')' group %prec IFX
    | IF '(' logical_expression ')' group ELSE group"""


def p_group(p):
    """group : if
    | while
    | for
    | line
    | block"""


def p_single_value(p):
    """single_value : ID
    | FLOAT
    | INT
    | STRING
    | matrix_definition"""


def p_select_element(p):
    """ select_element : matrix_definition matrix_row
    | ID matrix_row
    | '(' arithmetic_expression ')' matrix_row"""


def p_matrix_definition(p):
    """matrix_definition : '[' matrix_definition_inside ']'
     | matrix_gen_func """


def p_matrix_definition_inside(p):
    """matrix_definition_inside : matrix_row ',' matrix_definition_inside
    | matrix_row """


def p_matrix_row(p):
    """ matrix_row : '[' vector ']' """


def p_vector(p):
    """ vector : arithmetic_expression ',' vector
    | arithmetic_expression"""


def p_matrix_gen_func(p):
    """ matrix_gen_func : func_name '(' arithmetic_expression ')' """


def p_func_name(p):
    """ func_name : EYE
    | ONES
    | ZEROS """


def p_arithmetic_expression(p):
    """arithmetic_expression : arithmetic_expression '+' arithmetic_expression
    | arithmetic_expression '-' arithmetic_expression
    | arithmetic_expression '*' arithmetic_expression
    | arithmetic_expression '/' arithmetic_expression
    | arithmetic_expression MTX_SUM arithmetic_expression
    | arithmetic_expression MTX_DIFFERENCE arithmetic_expression
    | arithmetic_expression MTX_PRODUCT  arithmetic_expression
    | arithmetic_expression MTX_QUOTIENT  arithmetic_expression
    | single_value
    | '(' arithmetic_expression ')'
    | '-' arithmetic_expression %prec UMINUS
    | arithmetic_expression TRANSPOSE"""

# def p_arithmetic_expression(p):
#     """arithmetic_expression : arithmetic_expression arithmetic_operator arithmetic_expression
#     | single_value
#     | '(' arithmetic_expression ')'
#     | '-' arithmetic_expression %prec UMINUS
#     | arithmetic_expression TRANSPOSE"""


# def p_arithmetic_operator(p):
#     """ arithmetic_operator : '+'
#     | '-'
#     | '*'
#     | '/'
#     | MTX_SUM
#     | MTX_DIFFERENCE
#     | MTX_PRODUCT
#     | MTX_QUOTIENT """


def p_expression(p):
    """expression : assignment
    | BREAK
    | CONT
    | return
    | print """


def p_logical_expression(p):
    """logical_expression : arithmetic_expression comparison_operator arithmetic_expression"""


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
    """assignment : ID assignment_operator arithmetic_expression
    | select_element assignment_operator arithmetic_expression
    | select_element assignment_operator matrix_row"""


def p_print(p):
    """ print : PRINT vector"""


def p_return(p):
    """ return : RETURN arithmetic_expression
    | RETURN """


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


PARSER = yacc.yacc()



