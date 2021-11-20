import ply.yacc as yacc
import tree_draw as tree
from lexer import *

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', '+', '-', 'MTX_SUM', 'MTX_DIFFERENCE'),
    ('left', '*', '/', 'MTX_PRODUCT', 'MTX_QUOTIENT'),
    ('right', 'UMINUS'),
    ('left', 'TRANSPOSE')
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


def p_line1(p):
    """line : expression ';' """
    p[0]=tree.Node("line",[p[1],tree.Node(';',None)])


def p_line2(p):
    """line : ';' """
    p[0]=tree.Node("line",[tree.Node(';',None)])


def p_block(p):
    """block : '{' segment '}'"""
    p[0] = tree.Node("block", [tree.Node('{', None), p[2], tree.Node('}', None)])


def p_for(p):
    """for : FOR ID '=' range group """
    p[0] = tree.Node("FOR", [tree.Node('for', None), tree.Node("ID",[tree.Node(p[2],None)]), tree.Node('=', None),p[4],p[5]])


def p_range(p):
    """range : arithmetic_expression ':' arithmetic_expression """
    p[0] = tree.Node("range", [p[1], tree.Node(':', None), p[3]])


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""
    p[0] = tree.Node("while", [tree.Node('while', None), tree.Node('(', None), p[3], tree.Node(')', None), p[5]])


def p_if1(p):
    """if : IF '(' logical_expression ')' group %prec IFX"""
    p[0] = tree.Node("IF", [tree.Node('if', None),tree.Node('(', None),p[3],tree.Node(')', None),p[5]])


def p_if2(p):
    """if : IF '(' logical_expression ')' group ELSE group"""
    p[0] = tree.Node("IF", [tree.Node('if', None),tree.Node('(', None),p[3],tree.Node(')', None),p[5],tree.Node('else', None),p[7]])


def p_group(p):
    """group : if
    | while
    | for
    | line
    | block"""
    p[0] = tree.Node("group", [p[1]])


def p_single_valueID(p):
    """single_value : ID"""
    p[0] = tree.Node("single_value", [tree.Node("ID", [tree.Node(p[1], None)])])


def p_single_valueFLOAT(p):
    """single_value : FLOAT"""
    p[0] = tree.Node("single_value", [tree.Node("FLOAT", [tree.Node(p[1], None)])])


def p_single_valueINT(p):
    """single_value : INT"""
    p[0] = tree.Node("single_value", [tree.Node("INT", [tree.Node(p[1], None)])])


def p_single_valueSTRING(p):
    """single_value : STRING"""
    p[0] = tree.Node("single_value", [tree.Node("STRING", [tree.Node(p[1], None)])])


def p_single_valueMATRIX(p):
    """single_value : matrix_definition"""
    p[0] = tree.Node("single_value", [p[1]])


def p_select_elementMD(p):
    """ select_element : matrix_definition matrix_row"""
    p[0] = tree.Node("select_element", [p[1],p[2]])


def p_select_elementID(p):
    """ select_element : ID matrix_row"""
    p[0] = tree.Node("select_element", [tree.Node("ID", [tree.Node(p[1], None)]), p[2]])


def p_select_elementBAB(p):
    """ select_element : '(' arithmetic_expression ')' matrix_row"""
    p[0] = tree.Node("select_element", [tree.Node("(", None), p[2],tree.Node(")", None),p[4]])


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
    """ vector : arithmetic_expression ',' vector"""
    p[0]=tree.Node("vector",[p[1],tree.Node(",",None),p[3]])


def p_vector2(p):
    """ vector : arithmetic_expression"""
    p[0]=tree.Node("vector",[p[1]])


def p_matrix_gen_func(p):
    """ matrix_gen_func : func_name '(' arithmetic_expression ')' """
    p[0] = tree.Node("matrix_gen_func", [p[1],tree.Node("(",None),p[3],tree.Node(")",None)])


def p_func_name(p):
    """ func_name : EYE
    | ONES
    | ZEROS """
    p[0]=tree.Node("func_name",[tree.Node(p[1],None)])


# def p_arithmetic_expression(p):
#     """arithmetic_expression : arithmetic_expression '+' arithmetic_expression
#     | arithmetic_expression '-' arithmetic_expression
#     | arithmetic_expression '*' arithmetic_expression
#     | arithmetic_expression '/' arithmetic_expression
#     | arithmetic_expression MTX_SUM arithmetic_expression
#     | arithmetic_expression MTX_DIFFERENCE arithmetic_expression
#     | arithmetic_expression MTX_PRODUCT  arithmetic_expression
#     | arithmetic_expression MTX_QUOTIENT  arithmetic_expression
#     | single_value
#     | '(' arithmetic_expression ')'
#     | '-' arithmetic_expression %prec UMINUS
#     | arithmetic_expression TRANSPOSE"""


def p_arithmetic_expression1(p):
    """arithmetic_expression : arithmetic_expression '+' arithmetic_expression
    | arithmetic_expression '-' arithmetic_expression
    | arithmetic_expression '*' arithmetic_expression
    | arithmetic_expression '/' arithmetic_expression
    | arithmetic_expression MTX_SUM arithmetic_expression
    | arithmetic_expression MTX_DIFFERENCE arithmetic_expression
    | arithmetic_expression MTX_PRODUCT  arithmetic_expression
    | arithmetic_expression MTX_QUOTIENT  arithmetic_expression"""
    p[0] = tree.Node("arithmetic_expression", [p[1],tree.Node(p[2],None),p[3]])


def p_arithmetic_expression2(p):
    """arithmetic_expression : single_value"""
    p[0] = tree.Node("arithmetic_expression", [p[1]])


def p_arithmetic_expression3(p):
    """arithmetic_expression : arithmetic_expression TRANSPOSE """
    p[0] = tree.Node("arithmetic_expression", [p[1],tree.Node("TRANSPOSE",None)])


def p_arithmetic_expression4(p):
    """arithmetic_expression : '-' arithmetic_expression %prec UMINUS """
    p[0] = tree.Node("arithmetic_expression", [tree.Node("-",None),p[2]])


def p_arithmetic_expression5(p):
    """arithmetic_expression : '(' arithmetic_expression ')' """
    p[0] = tree.Node("arithmetic_expression", [tree.Node("(",None),p[2],tree.Node(")",None)])

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


def p_expression1(p):
    """expression : assignment
    | print
    | return """
    p[0] = tree.Node("expression", [p[1]])


def p_expression2(p):
    """expression : BREAK
    | CONT """
    p[0] = tree.Node("expression", [tree.Node(p[1],None)])


def p_logical_expression(p):
    """logical_expression : arithmetic_expression comparison_operator arithmetic_expression"""
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
    p[0] = tree.Node("assignment_operator", [tree.Node(p[1], None)])


def p_assignment1(p):
    """assignment : ID assignment_operator arithmetic_expression"""
    p[0] = tree.Node("assignment", [tree.Node("ID",[tree.Node(p[1],None)]),p[2],p[3]])


def p_assignment2(p):
    """assignment : select_element assignment_operator arithmetic_expression"""
    p[0] = tree.Node("assignment", [p[1],p[2],p[3]])


def p_assignment3(p):
    """assignment : select_element assignment_operator matrix_row"""
    p[0] = tree.Node("assignment", [p[1], p[2], p[3]])


def p_print(p):
    """ print : PRINT vector"""
    p[0] = tree.Node("print", [tree.Node("PRINT",None),p[2]])


def p_return1(p):
    """ return : RETURN arithmetic_expression """
    p[0] = tree.Node("return", [tree.Node("RETURN", None), p[2]])


def p_return2(p):
    """ return : RETURN """
    p[0] = tree.Node("return", [tree.Node("RETURN", None)])


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parserA = yacc.yacc()



