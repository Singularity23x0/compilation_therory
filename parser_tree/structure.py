class Node:
    def __init__(self):
        self.line = None

    def set_line(self, line):
        self.line = line
        return self

    def get_line(self):
        return "Line unknown: " if self.line is None else "At line {}: ".format(self.line)


class Segment(Node):
    def __init__(self, el, segment=None):
        if el is None:
            self.instructionList = None
        else:
            if segment is None:
                self.instructionList = [el]
            elif segment.instructionList is not None:
                self.instructionList = [el] + segment.instructionList


class Block(Node):
    def __init__(self, segment):
        self.segment = segment
        # other


class For(Node):
    def __init__(self, idv, rangeS, inside):
        self.idv = idv
        self.rangeS = rangeS
        self.inside = inside


class Range(Node):
    def __init__(self, fro, to):
        self.fro = fro
        self.to = to


class While(Node):
    def __init__(self, condition, inside):
        self.condition = condition
        self.inside = inside


class If(Node):
    def __init__(self, condition, inside):
        self.condition = condition
        self.inside = inside


class IfElse(Node):
    def __init__(self, condition, inside, inside_else):
        self.condition = condition
        self.inside = inside
        self.insideElse = inside_else


class Types(Node):
    UNDEFINED = 0
    INT = 1
    FLOAT = 2
    STRING = 3
    COLUMN = 5
    T = ["UNDEFINED", "INT", "FLOAT", "STRING", "COLUMN"]

    def typeName(i):
        return Types.T[i]


def types_equivalent(type1, type2):
    if min(type1, type2) == 0:
        return True
    if max(type1, type2) <= 2:
        return True
    return type1 == type2


def types_strong_equivalent(type1, type2):
    if min(type1, type2) == 0:
        return True
    return type1 == type2


def get_type(val):  # TODO make
    if isinstance(val, int):
        return Types.INT
    if isinstance(val, float):
        return Types.FLOAT
    if isinstance(val, str):
        return Types.STRING
    return val.core_type


class Value(Node):  # is_matrix : 0 -> false, 1 -> true, -1 -> unknown
    def __init__(self, value, is_matrix=0, const=False):
        self.const = const
        self.value = value


class Variable(Node):
    def __init__(self, name, variable_type=Types.UNDEFINED):
        self.name = name
        self.type = variable_type


class SelectionSingle(Node):
    def __init__(self, matrix, pos1, pos2):
        self.matrix = matrix
        self.pos1 = pos1
        self.pos2 = pos2


class SelectRow(Node):
    def __init__(self, matrix, pos):
        self.matrix = matrix

        self.pos = pos


class Matrix(Node):
    def __init__(self, rows_list):
        self.rows_list = rows_list

        self.rows_amount = len(rows_list)
        self.columns_amount = rows_list[0].size


class Row(Node):
    def __init__(self, values_list):
        self.values_list = values_list

        self.size = len(values_list)

    def getSize(self):
        return self.size

    def getFirst(self):
        return self.values_list[0]

    def getSecond(self):
        return self.values_list[1]


class Vector(Node):
    def __init__(self, value=None, vec=None):
        self.value = list()
        if value is not None:
            self.value.append(value)

        if vec is not None:
            self.value += vec.value

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]


class Function(Node):
    def __init__(self, name, argument):
        self.name = name
        self.arguments = argument


class Operator:
    PLUS = 1
    MINUS = 2
    STAR = 3
    SLASH = 4
    MPLUS = 5
    MMINUS = 6
    MSTAR = 7
    MSLASH = 8
    UMINUS = 9
    TRANSPOSE = 10
    T = ["PLUS",
         "MINUS",
         "STAR",
         "SLASH",
         "MPLUS",
         "MMINUS",
         "MSTAR",
         "MSLASH",
         "UMINUS",
         "TRANSPOSE"]

    def operator_name(self):
        return Operator.T[self - 1]


class ArithmeticExpressionUnary(Node):
    def __init__(self, element, operator):
        self.element = element
        self.operator = operator


class ArithmeticExpressionBinary(Node):
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator


class LogicalExpression(Node):
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator


class Assignment(Node):
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator


class Print(Node):
    def __init__(self, vector):
        self.vector = vector


class Return(Node):
    def __init__(self, value):
        self.value = value


class Break(Node):
    pass


class Cont(Node):
    pass


class Empty(Node):
    pass
