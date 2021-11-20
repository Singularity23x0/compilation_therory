import ply.yacc as yacc
from abstract_parser_tree.structure import *
from lexer import *
from abstract_parser_tree.draw import TreePrinter

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
    p[0] = Block(p[1])
    TreePrinter("resART.txt").draw(p[0])


def p_program2(p):
    """program : """
    print("empty")


def p_segment1(p):
    """segment : group segment"""
    p[0] = Segment(p[1], p[2])


def p_segment2(p):
    """segment : group"""
    p[0] = Segment(p[1])


def p_line1(p):
    """line : expression ';' """
    p[0] = p[1]


def p_line2(p):
    """line : ';' """
    p[0] = Empty()


def p_block(p):
    """block : '{' segment '}'"""
    p[0] = Block(p[2])


def p_for(p):
    """for : FOR ID '=' range group """
    p[0] = For(Variable(p[2], Types.INT), p[4], p[5])


def p_range(p):
    """range : arithmetic_expression ':' arithmetic_expression """
    p[0] = Range(p[1], p[3])


def p_while(p):
    """while : WHILE '(' logical_expression ')' group"""
    p[0] = While(p[3], p[5])


def p_if1(p):
    """if : IF '(' logical_expression ')' group %prec IFX"""
    p[0] = If(p[3], p[5])


def p_if2(p):
    """if : IF '(' logical_expression ')' group ELSE group"""
    p[0] = IfElse(p[3], p[5], p[7])


def p_group(p):
    """group : if
    | while
    | for
    | line
    | block"""
    p[0] = p[1]


def p_single_valueID(p):
    """single_value : ID"""
    p[0] = Variable(p[1])


def p_single_valueFLOAT(p):
    """single_value : FLOAT"""
    p[0] = Value(p[1], Types.FLOAT,True)


def p_single_valueINT(p):
    """single_value : INT"""
    p[0] = Value(p[1], Types.INT,True)


def p_single_valueSTRING(p):
    """single_value : STRING"""
    p[0] = Value(p[1], Types.STRING,True)


def p_single_valueMATRIX(p):
    """single_value : matrix_definition"""
    p[0] = Value(p[1], Types.MATRIX,True)


def p_select_elementMD(p):
    """ select_element : matrix_definition matrix_row"""
    if p[2].getSize() == 2:
        p[0] = SelectionSingle(p[1], p[2].getFirst(), p[2].getSecont())
    elif p[2].getSize() == 1:
        p[0] = SelectColumn(p[1], p[2].getFirst())
    else:
        raise ValueError("error wrong index list size in {0}".format(p.lineno))


def p_select_elementID(p):
    """ select_element : ID matrix_row"""
    if p[2].getSize() == 2:
        p[0] = SelectionSingle(Variable(p[1], Types.MATRIX), p[2].getFirst(), p[2].getSecond())
    elif p[2].getSize() == 1:
        p[0] = SelectColumn(Variable(p[1], Types.MATRIX), p[2].getFirst())
    else:
        raise ValueError("error wrong index list size in {0}".format(p.lineno))


def p_select_elementBAB(p):
    """ select_element : '(' arithmetic_expression ')' matrix_row"""
    if p[2].getSize() == 2:
        p[0] = SelectionSingle(Value(p[2], Types.MATRIX), p[4].getFirst(), p[4].getSecont())
    elif p[2].getSize() == 1:
        p[0] = SelectColumn(Value(p[2], Types.MATRIX), p[2].getFirst())
    else:
        raise ValueError("error wrong index list size in {0}".format(p.lineno))


def p_matrix_definition1(p):
    """matrix_definition : '[' matrix_definition_inside ']' """
    p[0] = Value(Matrix(p[2]), Types.MATRIX)


def p_matrix_definition2(p):
    """matrix_definition : matrix_gen_func """
    p[0] = Value(p[1], Types.MATRIX)


def p_matrix_definition_inside1(p):
    """matrix_definition_inside : matrix_row ',' matrix_definition_inside"""
    p[0] = [p[1]] + p[3]


def p_matrix_definition_inside2(p):
    """matrix_definition_inside : matrix_row """
    p[0] = [p[1]]


def p_matrix_row(p):
    """ matrix_row : '[' vector ']' """
    p[0] = Row(p[2])


def p_vector1(p):
    """ vector : arithmetic_expression ',' vector"""
    p[0] = Vector(p[1], p[3])


def p_vector2(p):
    """ vector : arithmetic_expression"""
    p[0] = Vector(p[1])


def p_matrix_gen_func(p):
    """ matrix_gen_func : func_name '(' arithmetic_expression ')' """
    p[0] = Function(p[1],p[3])


def p_func_name(p):
    """ func_name : EYE
    | ONES
    | ZEROS """
    p[0] = p[1]


def p_arithmetic_expression1p(p):
    """arithmetic_expression : arithmetic_expression '+' arithmetic_expression"""
    p[0] = ArithmeticExpressionBinary(p[1],p[3],Operator.PLUS)


def p_arithmetic_expression1m(p):
    """arithmetic_expression : arithmetic_expression '-' arithmetic_expression"""
    p[0] = ArithmeticExpressionBinary(p[1],p[3],Operator.MINUS)


def p_arithmetic_expression1st(p):
    """arithmetic_expression : arithmetic_expression '*' arithmetic_expression"""
    p[0] = ArithmeticExpressionBinary(p[1],p[3],Operator.STAR)


def p_arithmetic_expression1sl(p):
    """arithmetic_expression : arithmetic_expression '/' arithmetic_expression"""
    p[0] = ArithmeticExpressionBinary(p[1],p[3],Operator.SLASH)


def p_arithmetic_expression1(p):
    """arithmetic_expression : arithmetic_expression MTX_SUM arithmetic_expression"""
    p[0] = ArithmeticExpressionBinary(p[1],p[3],Operator.MPLUS)


def p_arithmetic_expression1MM(p):
    """arithmetic_expression : arithmetic_expression MTX_DIFFERENCE arithmetic_expression"""
    p[0] = ArithmeticExpressionBinary(p[1],p[3],Operator.PLUS)


def p_arithmetic_expression1mst(p):
    """arithmetic_expression : arithmetic_expression MTX_PRODUCT  arithmetic_expression"""
    p[0] = ArithmeticExpressionBinary(p[1],p[3],Operator.MSTAR)


def p_arithmetic_expression1msl(p):
    """arithmetic_expression : arithmetic_expression MTX_QUOTIENT  arithmetic_expression"""
    p[0] = ArithmeticExpressionBinary(p[1],p[3],Operator.MSLASH)


def p_arithmetic_expression2(p):
    """arithmetic_expression : single_value"""
    p[0] = p[1]


def p_arithmetic_expression3(p):
    """arithmetic_expression : arithmetic_expression TRANSPOSE """
    p[0] = ArithmeticExpressionUnary(p[1],Operator.TRANSPOSE)


def p_arithmetic_expression4(p):
    """arithmetic_expression : '-' arithmetic_expression %prec UMINUS """
    p[0] = ArithmeticExpressionUnary(p[2],Operator.UMINUS)


def p_arithmetic_expression5(p):
    """arithmetic_expression : '(' arithmetic_expression ')' """
    p[0] = p[2]


def p_expression1(p):
    """expression : assignment
    | print
    | return """
    p[0] = p[1]


def p_expression2(p):
    """expression : BREAK"""
    p[0] = Break()


def p_expression3(p):
    """expression : CONT """
    p[0] = Cont()


def p_logical_expression(p):
    """logical_expression : arithmetic_expression comparison_operator arithmetic_expression"""
    p[0] = LogicalExpression(p[1],p[3],p[2])


def p_comparison_operator(p):
    """comparison_operator : '<'
    | '>'
    | EQUAL
    | NOT_EQUAL
    | SMALLER_OR_EQUAL
    | LARGER_OR_EQUAL"""
    p[0] = p[1]  # TODO add enum


def p_assignment_operator(p):
    """assignment_operator : '='
    | ADD
    | SUBTRACT
    | MULTIPLY
    | DIVIDE """
    p[0] = p[1]  # TODO add enum


def p_assignment1(p):
    """assignment : ID assignment_operator arithmetic_expression"""
    p[0] = Assignment(Variable(p[1]),p[3],p[2])


def p_assignment2(p):
    """assignment : select_element assignment_operator arithmetic_expression"""
    p[0] = Assignment(p[1],p[3],p[2])


def p_assignment3(p):
    """assignment : select_element assignment_operator matrix_row"""
    p[0] = Assignment(p[1], p[3], p[2])


def p_print(p):
    """ print : PRINT vector"""
    p[0] = Print(p[2])


def p_return1(p):
    """ return : RETURN arithmetic_expression """
    p[0] = Return(p[2])


def p_return2(p):
    """ return : RETURN """
    p[0] = Return(Empty())


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


PARSER = yacc.yacc()