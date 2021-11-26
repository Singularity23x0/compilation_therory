class Segment:
    def __init__(self, el, segment=None):
        if el is None:
            self.instructionList = None
        else:
            if segment is None:
                self.instructionList = [el]
            elif segment.instructionList is not None:
                self.instructionList = [el] + segment.instructionList


class Block:
    def __init__(self, segment):
        self.segment = segment
        # other


class For:
    def __init__(self, idv, rangeS, inside):
        self.idv = idv
        self.rangeS = rangeS
        self.inside = inside


class Range:
    def __init__(self, fro, to):
        if not (types_strong_equivalent(fro.type, Types.INT) and types_strong_equivalent(to.type, Types.INT)):
            raise ValueError("Range must be an INT")
        self.fro = fro
        self.to = to


class While:
    def __init__(self, condition, inside):
        self.condition = condition
        self.inside = inside


class If:
    def __init__(self, condition, inside):
        self.condition = condition
        self.inside = inside


class IfElse:
    def __init__(self, condition, inside, insideElse):
        self.condition = condition
        self.inside = inside
        self.insideElse = insideElse


class Types:  # enum for types
    UNDEFINED = 0
    INT = 1
    FLOAT = 2
    STRING = 3
    MATRIX = 4
    COLUMN = 5
    T = ["UNDEFINED", "INT", "FLOAT", "STRING", "MATRIX", "COLUMN"]

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


class Value:
    def __init__(self, value, value_type, const=False):  # TODO auto const
        self.const = const
        self.value = value
        self.type = value_type


class Variable:
    def __init__(self, name, variable_type=Types.UNDEFINED):
        self.name = name
        self.type = variable_type


class SelectionSingle:  # TODO change name
    def __init__(self, matrix, pos1, pos2):
        if not (types_strong_equivalent(pos1.type, Types.INT) and types_strong_equivalent(pos2.type, Types.INT)):
            raise ValueError("Matrix indices must be of the INT type")
        self.matrix = matrix
        self.pos1 = pos1
        self.pos2 = pos2


class SelectColumn:
    def __init__(self, matrix, pos):
        if not types_strong_equivalent(pos.type, Types.INT):
            raise ValueError("Matrix indices must be of the INT type")
        self.matrix = matrix
        self.pos = pos


class Matrix:
    def __init__(self, rows_list):
        self.rows_list = rows_list
        self.type = Types.UNDEFINED  # TODO findIt
        self.row_size = 0  # TODO calculate it
        self.columns_amount = len(rows_list)  # TODO change name


class Row:
    def __init__(self, values_list):
        self.values_list = values_list
        self.type = Types.UNDEFINED  # TODO findIt
        self.size = len(values_list)

    def getSize(self):
        return self.size

    def getFirst(self):
        return self.values_list[0]

    def getSecond(self):
        return self.values_list[1]


class Vector:
    def __init__(self, value=None, vec=None):
        self.value = list()
        if value is not None:
            self.value.append(value)

        if vec is not None:
            if type(vec) is Vector:
                self.value += vec.value
            else:
                raise ValueError("wrong val in vec for Vector is {0} not {1}".format(type(vec), Vector))

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]


class Function:
    def __init__(self, name, argument):  # returnType):
        if not types_strong_equivalent(argument.type, Types.INT):
            raise ValueError("The argument of {} must be an INT".format(name))
        self.name = name
        self.arguments = argument
        # self.returnType=returnType #no needed always matrix


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


class ArithmeticExpressionUnary:
    def __init__(self, element, operator):
        if operator == Operator.TRANSPOSE and not types_equivalent(element.type, Types.MATRIX):
            raise ValueError("Transposition operator used with invalid type {}".format(Types.typeName(element.type)))
        self.element = element
        self.operator = operator
        self.type = element.type


class ArithmeticExpressionBinary:
    def __init__(self, left, right, operator):
        if not types_equivalent(left.type, right.type):
            raise ValueError("{} data type incompatible with {}"
                             .format(Types.typeName(left.type), Types.typeName(right.type)))
        if operator > 4 and not types_equivalent(left.type, Types.MATRIX):
            raise ValueError("Type {} not compatible with the operator {}"
                             .format(Types.typeName(max(left.type, right.type)), Operator.operator_name(operator)))
        self.left = left
        self.right = right
        self.operator = operator
        self.type = max(left.type, right.type)


class LogicalExpression:
    def __init__(self, left, right, operator):  # TODO matching types
        self.left = left
        self.right = right
        self.operator = operator


class Assignment:
    def __init__(self, left, right, operator):  # TODO matching types and operators
        self.left = left
        self.right = right
        self.operator = operator


class Print:
    def __init__(self, vector):
        self.vector = vector


class Return:
    def __init__(self, value):
        self.value = value


class Break:
    pass


class Cont:
    pass


class Empty:
    pass
