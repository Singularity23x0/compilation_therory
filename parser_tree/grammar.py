import ply.yacc as yacc
from parser_tree.structure import *
from lexer import *

tree_structure = None
err = False


def get_structure():
    if err:
        return None
    return tree_structure


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
    p[0] = Block(p[1],True).set_line(p.lineno(1))
    global tree_structure
    tree_structure = p[0]


def p_program2(p):
    """program : """
    print("empty")


def p_segment1(p):
    """segment : group segment"""
    p[0] = Segment(p[1], p[2]).set_line(p.lineno(1))


def p_segment2(p):
    """segment : group"""
    p[0] = Segment(p[1]).set_line(p.lineno(1))


def p_line1(p):
    """line : expression ';' """
    p[0] = p[1]


def p_line2(p):
    """line : ';' """
    p[0] = Empty().set_line(p.lineno(1))


def p_block(p):
    """block : '{' segment '}'"""
    p[0] = Block(p[2]).set_line(p.lineno(1))


def p_for(p):
    """for : FOR ID '=' range group """
    p[0] = For(Variable(p[2], Types.INT), p[4], p[5]).set_line(p.lineno(1))


def p_range(p):
    """range : arithmetic_expression ':' arithmetic_expression """
    p[0] = Range(p[1], p[3]).set_line(p.lineno(1))


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""
    p[0] = While(p[3], p[5]).set_line(p.lineno(1))


def p_if1(p):
    """if : IF '(' logical_expression ')' group %prec IFX"""
    p[0] = If(p[3], p[5]).set_line(p.lineno(1))


def p_if2(p):
    """if : IF '(' logical_expression ')' group ELSE group"""
    p[0] = IfElse(p[3], p[5], p[7]).set_line(p.lineno(1))


def p_group(p):
    """group : if
    | while
    | for
    | line
    | block"""
    p[0] = p[1]


def p_single_value_ID(p):
    """single_value : ID"""
    p[0] = Variable(p[1]).set_line(p.lineno(1))


def p_single_value_FLOAT(p):
    """single_value : FLOAT"""
    p[0] = Value(p[1], const=True).set_line(p.lineno(1))


def p_single_value_INT(p):
    """single_value : INT"""
    p[0] = Value(p[1], const=True).set_line(p.lineno(1))


def p_single_valueSTRING(p):
    """single_value : STRING"""
    p[0] = Value(p[1], const=True).set_line(p.lineno(1))


def p_single_value_MATRIX(p):
    """single_value : matrix_definition"""
    p[0] = Value(p[1], is_matrix=1, const=True).set_line(p.lineno(1))


def p_select_element_MD(p):
    """ select_element : matrix_definition matrix_row"""
    if p[2].getSize() == 2:
        p[0] = SelectionSingle(p[1], p[2].getFirst(), p[2].getSecont()).set_line(p.lineno(1))
    elif p[2].getSize() == 1:
        p[0] = SelectRow(p[1], p[2].getFirst()).set_line(p.lineno(1))


def p_select_element_ID(p):
    """ select_element : ID matrix_row"""
    if p[2].getSize() == 2:
        p[0] = SelectionSingle(Variable(p[1]), p[2].getFirst(), p[2].getSecond()).set_line(p.lineno(1))
    elif p[2].getSize() == 1:
        p[0] = SelectRow(Variable(p[1]), p[2].getFirst()).set_line(p.lineno(1))


def p_select_element_BAB(p):
    """ select_element : '(' arithmetic_expression ')' matrix_row"""
    if p[4].getSize() == 2:
        p[0] = SelectionSingle(p[2], p[4].getFirst(), p[4].getSecond()).set_line(p.lineno(1))
    elif p[4].getSize() == 1:
        p[0] = SelectRow(p[2], p[4].getFirst()).set_line(p.lineno(1))


def p_matrix_definition(p):
    """matrix_definition : '[' matrix_definition_inside ']' """
    p[0] = Matrix(p[2]).set_line(p.lineno(1))


def p_matrix_definition_by_function(p):
    """matrix_definition : matrix_gen_func """
    p[0] = p[1]


def p_matrix_definition_inside_multi_row(p):
    """matrix_definition_inside : matrix_row ',' matrix_definition_inside"""
    p[0] = [p[1]] + p[3]


def p_matrix_definition_inside(p):
    """matrix_definition_inside : matrix_row """
    p[0] = [p[1]]


def p_matrix_row(p):
    """ matrix_row : '[' vector ']' """
    p[0] = Row(p[2]).set_line(p.lineno(1))


def p_vector_multi_expression(p):
    """ vector : arithmetic_expression ',' vector"""
    p[0] = Vector(p[1], p[3]).set_line(p.lineno(1))


def p_vector_expression(p):
    """ vector : arithmetic_expression"""
    p[0] = Vector(p[1]).set_line(p.lineno(1))


def p_matrix_gen_func(p):
    """ matrix_gen_func : func_name '(' arithmetic_expression ')' """
    p[0] = Function(p[1], p[3]).set_line(p.lineno(1))


def p_func_name(p):
    """ func_name : EYE
    | ONES
    | ZEROS """
    p[0] = p[1]


def create_arithmetic_expression(p, operator):
    p[0] = ArithmeticExpressionBinary(p[1], p[3], operator).set_line(p.lineno(1))


def p_arithmetic_expression1_add(p):
    """arithmetic_expression : arithmetic_expression '+' arithmetic_expression"""
    create_arithmetic_expression(p, Operator.PLUS)


def p_arithmetic_expression1_subtract(p):
    """arithmetic_expression : arithmetic_expression '-' arithmetic_expression"""
    create_arithmetic_expression(p, Operator.MINUS)


def p_arithmetic_expression1_multiply(p):
    """arithmetic_expression : arithmetic_expression '*' arithmetic_expression"""
    create_arithmetic_expression(p, Operator.STAR)


def p_arithmetic_expression1_divide(p):
    """arithmetic_expression : arithmetic_expression '/' arithmetic_expression"""
    create_arithmetic_expression(p, Operator.SLASH)


def p_arithmetic_expression1_mtx_add(p):
    """arithmetic_expression : arithmetic_expression MTX_SUM arithmetic_expression"""
    create_arithmetic_expression(p, Operator.MPLUS)


def p_arithmetic_expression1_mtx_subtract(p):
    """arithmetic_expression : arithmetic_expression MTX_DIFFERENCE arithmetic_expression"""
    create_arithmetic_expression(p, Operator.MMINUS)


def p_arithmetic_expression1_mtx_multiply(p):
    """arithmetic_expression : arithmetic_expression MTX_PRODUCT  arithmetic_expression"""
    create_arithmetic_expression(p, Operator.MSTAR)


def p_arithmetic_expression1_mtx_divide(p):
    """arithmetic_expression : arithmetic_expression MTX_QUOTIENT  arithmetic_expression"""
    create_arithmetic_expression(p, Operator.MSLASH)


def p_arithmetic_expression2(p):
    """arithmetic_expression : single_value"""
    p[0] = p[1]


def p_arithmetic_expression3(p):
    """arithmetic_expression : arithmetic_expression TRANSPOSE """
    p[0] = ArithmeticExpressionUnary(p[1], Operator.TRANSPOSE).set_line(p.lineno(1))


def p_arithmetic_expression4(p):
    """arithmetic_expression : '-' arithmetic_expression %prec UMINUS """
    p[0] = ArithmeticExpressionUnary(p[2], Operator.UMINUS).set_line(p.lineno(1))


def p_arithmetic_expression5(p):
    """arithmetic_expression : '(' arithmetic_expression ')' """
    p[0] = p[2]


def p_expression(p):
    """expression : assignment
    | print
    | return """
    p[0] = p[1]


def p_expression_break(p):
    """expression : BREAK"""
    p[0] = Break().set_line(p.lineno(1))


def p_expression_continue(p):
    """expression : CONT """
    p[0] = Cont().set_line(p.lineno(1))


def p_logical_expression(p):
    """logical_expression : arithmetic_expression comparison_operator arithmetic_expression"""
    p[0] = LogicalExpression(p[1], p[3], p[2]).set_line(p.lineno(1))


def p_comparison_operator(p):
    """comparison_operator : '<'
    | '>'
    | EQUAL
    | NOT_EQUAL
    | SMALLER_OR_EQUAL
    | LARGER_OR_EQUAL"""
    p[0] = p[1]


def p_assignment_operator(p):
    """assignment_operator : '='
    | ADD
    | SUBTRACT
    | MULTIPLY
    | DIVIDE """
    p[0] = p[1]


def create_assignment(p):
    p[0] = Assignment(p[1], p[3], p[2]).set_line(p.lineno(1))


def p_assignment1(p):
    """assignment : ID assignment_operator arithmetic_expression"""
    p[0] = Assignment(Variable(p[1]), p[3], p[2]).set_line(p.lineno(1))


def p_assignment11(p):
    """assignment : ID assignment_operator select_element"""
    p[0] = Assignment(Variable(p[1]), p[3], p[2]).set_line(p.lineno(1))


def p_assignment2(p):
    """assignment : select_element assignment_operator arithmetic_expression"""
    create_assignment(p)


def p_assignment3(p):
    """assignment : select_element assignment_operator matrix_row"""
    create_assignment(p)


def p_assignment4(p):
    """assignment : select_element assignment_operator select_element"""
    create_assignment(p)


def p_print(p):
    """ print : PRINT vector"""
    p[0] = Print(p[2]).set_line(p.lineno(1))


def p_return1(p):
    """ return : RETURN arithmetic_expression """
    p[0] = Return(p[2]).set_line(p.lineno(1))


def p_return2(p):
    """ return : RETURN """
    p[0] = Return(Empty()).set_line(p.lineno(1))


def p_error(p):
    global err
    err = True
    if p:
        print("Syntax error at line {}: LexToken('{}')".format(p.lineno, p.value))
    else:
        print("Unexpected end of input")


PARSER = yacc.yacc()
