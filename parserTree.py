import ply.yacc as yacc
import tree_draw as tree
from lexer import *

precedence = (
    #('nonassoc', 'EQUAL','NOT_EQUAL','SMALLER_OR_EQUAL','LARGER_OR_EQUAL'),
    #('nonassoc', 'ARITH_EXP'),
    #('nonassoc', 'FLOAT'),
    #('nonassoc', 'INT'),
    #('nonassoc', 'STRING'),
# ('nonassoc', 'LINE'),
    ('nonassoc', 'RANGE'),  # check if should be here
    ('nonassoc', 'IFN'),  # check if should be here
    ('nonassoc', 'IFX'),
    #('right', '='),
    ('left', 'ART'),  # check if should be here
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'MTX_SUM', 'MTX_DIFFERENCE'),
    ('left', 'MTX_PRODUCT', 'MTX_QUOTIENT'),
    ('right', 'UMINUS'),
    ('left', 'TRANSPOSE'),
)


def p_program1(p):
    """program : segment"""
    tree.Node("Program",[p[1]]).draw("res.txt")


def p_program2(p):
    """program : """
    print("empty")


def p_segment1(p):
    """segment : group segment"""
    p[0]=tree.Node("segment",[p[1],p[2]])


def p_segment2(p):
    """segment : group"""
    p[0]=tree.Node("segment",[p[1]])


def p_line(p):
    """line : expression ';' """
    p[0]=tree.Node("line",[p[1],tree.Node(';',None)])


def p_block(p):
    """block : '{' segment '}'"""
    p[0] = tree.Node("block", [tree.Node('{', None), p[2], tree.Node('}', None)])


def p_for(p):
    """for : FOR ID '=' range group """
    p[0] = tree.Node("for", [tree.Node('for', None), tree.Node("ID",[tree.Node(p[2],None)]), tree.Node('=', None),p[4],p[5]])


def p_range(p):
    """range : value_element ':' value_element %prec RANGE"""
    p[0] = tree.Node("range", [p[1],tree.Node(':', None), p[3]])


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""
    p[0] = tree.Node("while", [tree.Node('while', None),tree.Node('(', None),p[3],tree.Node(')', None),p[5]])


def p_if1(p):
    """if : IF '(' logical_expression ')' group %prec IFN"""
    p[0] = tree.Node("if", [tree.Node('if', None),tree.Node('(', None),p[3],tree.Node(')', None),p[5]])


def p_if2(p):
    """if : IF '(' logical_expression ')' group ELSE group %prec IFX"""
    p[0] = tree.Node("if", [tree.Node('if', None),tree.Node('(', None),p[3],tree.Node(')', None),p[5],tree.Node('else', None),p[7]])


def p_group(p):
    """group : conditional
    | line
    | block"""
    p[0] = tree.Node("group", [p[1]])


def p_conditional(p):
    """conditional : if
    | while
    | for"""
    p[0] = tree.Node("conditional", [p[1]])


def p_value_element11(p):
    """value_element : ID"""
    p[0] = tree.Node("value_element", [tree.Node("ID",[tree.Node(p[1],None)])])


def p_value_element12(p):
    """value_element : FLOAT"""
    p[0] = tree.Node("value_element", [tree.Node("FLOAT",[tree.Node(p[1],None)])])


def p_value_element13(p):
    """value_element : INT"""
    p[0] = tree.Node("value_element", [tree.Node("INT",[tree.Node(p[1],None)])])


def p_value_element14(p):
    """value_element : STRING """
    p[0] = tree.Node("value_element", [tree.Node("STRING",[tree.Node(p[1],None)])])


def p_value_element2(p):
    """value_element : arithmetic_expression
    | matrix_definition"""
    p[0] = tree.Node("value_element", [p[1]])


def p_value_element3(p):
    """value_element : '-' value_element %prec UMINUS"""
    p[0] = tree.Node("value_element", [tree.Node("-",None),p[2]])


def p_value_element4(p):
    """value_element : value_element TRANSPOSE"""
    p[0] = tree.Node("value_element", [p[1],tree.Node("'",None)])


def p_matrix_definition1(p):
    """matrix_definition : '[' matrix_definition_inside ']' """
    p[0] = tree.Node("matrix_definition", [tree.Node("[",None),p[2],tree.Node("]",None)])


def p_matrix_definition2(p):
    """matrix_definition : matrix_gen_func """
    p[0] = tree.Node("matrix_definition", [p[1]])


def p_matrix_definition_inside1(p):
    """matrix_definition_inside : matrix_row ',' matrix_definition_inside"""
    p[0]=tree.Node("matrix_definition_inside",[p[1],tree.Node(",",None),p[3]])


def p_matrix_definition_inside2(p):
    """matrix_definition_inside : matrix_row """
    p[0]=tree.Node("matrix_definition_inside",[p[1]])


def p_matrix_row(p):
    """ matrix_row : '[' vector ']' """
    p[0] = tree.Node("matrix_row", [tree.Node("[",None),p[2],tree.Node("]",None)])


def p_vector1(p):
    """ vector : value_element ',' vector"""
    p[0]=tree.Node("vector",[p[1],tree.Node(",",None),p[3]])


def p_vector2(p):
    """ vector : value_element"""
    p[0]=tree.Node("vector",[p[1]])


def p_matrix_gen_func(p):
    """ matrix_gen_func : func_name '(' value_element ')' """
    p[0] = tree.Node("matrix_gen_func", [p[1],tree.Node("(",None),p[3],tree.Node(")",None)])


def p_func_name(p):
    """ func_name : EYE
    | ONES
    | ZEROS """
    p[0]=tree.Node("func_name",[tree.Node(p[1],None)])


def p_arithmetic_expression1(p):
    """arithmetic_expression : value_element arithmetic_operator value_element %prec ART"""
    p[0] = tree.Node("arithmetic_expression", [p[1],p[2],p[3]])


def p_arithmetic_expression2(p):
    """arithmetic_expression : '(' value_element ')' """
    p[0] = tree.Node("arithmetic_expression", [tree.Node("(",None),p[2],tree.Node(")",None)])


def p_arithmetic_operator(p):
    """ arithmetic_operator : '+'
    | '-'
    | '*'
    | '/'
    | MTX_SUM
    | MTX_DIFFERENCE
    | MTX_PRODUCT
    | MTX_QUOTIENT """
    p[0]=tree.Node("arithmetic_operator",[tree.Node(p[1],None)])


def p_expression1(p):
    """expression : logical_expression
    | assignment
    | value_element
    | print """
    p[0] = tree.Node("expression", [p[1]])


def p_expression2(p):
    """expression : BREAK
    | CONT
    | RETURN"""
    p[0] = tree.Node("expression", [tree.Node(p[1],None)])


def p_logical_expression(p):
    """logical_expression : value_element comparison_operator value_element"""
    p[0] = tree.Node("logical_expression", [p[1],p[2],p[3]])


def p_comparison_operator(p):
    """comparison_operator : '<'
    | '>'
    | EQUAL
    | NOT_EQUAL
    | SMALLER_OR_EQUAL
    | LARGER_OR_EQUAL"""
    p[0]=tree.Node("comparison_operator",[tree.Node(p[1],None)])


def p_assignment_operator(p):
    """assignment_operator : '='
    | ADD
    | SUBTRACT
    | MULTIPLY
    | DIVIDE """
    p[0]=tree.Node("assignment_operator",[tree.Node(p[1],None)])


def p_assignment(p):
    """assignment : ID assignment_operator value_element"""
    p[0] = tree.Node("assignment", [tree.Node("ID",[tree.Node(p[1],None)]),p[2],p[3]])


def p_print(p):
    """ print : PRINT vector"""
    p[0] = tree.Node("print", [tree.Node("PRINT",None),p[2]])


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parserA = yacc.yacc()



