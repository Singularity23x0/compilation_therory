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
    def __init__(self, condition, inside, inside_else):
        self.condition = condition
        self.inside = inside
        self.insideElse = inside_else


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


def get_type(val):  # TODO make
    if isinstance(val,int):
        return Types.INT
    if isinstance(val,float):
        return Types.FLOAT
    if isinstance(val,str):
        return Types.STRING
    return val.type


class Value:  # is_matrix : 0 -> false, 1 -> true, -1 -> unknown
    def __init__(self, value, is_matrix=0, const=False):
        self.const = const
        self.value = value
        self.type = get_type(value)
        self.is_matrix = is_matrix


class Variable:
    def __init__(self, name, variable_type=Types.UNDEFINED):
        self.name = name
        self.type = variable_type
        self.is_matrix = -1


class SelectionSingle:
    def __init__(self, matrix, pos1, pos2):
        if not (types_strong_equivalent(pos1.type, Types.INT) and types_strong_equivalent(pos2.type, Types.INT)):
            raise ValueError("Matrix indices must be of the INT type")
        self.matrix = matrix
        self.pos1 = pos1
        self.pos2 = pos2
        self.type = matrix.type


class SelectRow:
    def __init__(self, matrix, pos):
        if not types_strong_equivalent(pos.type, Types.INT):
            raise ValueError("Matrix indices must be of the INT type")
        self.matrix = matrix
        self.type = matrix.type
        self.pos = pos


class Matrix:
    def __init__(self, rows_list):
        self.rows_list = rows_list
        self.type = analyze_types(rows_list)
        if self.type is None:
            raise ValueError("Matrix rows must be of compatible types")
        self.rows_amount = len(rows_list)
        self.columns_amount = rows_list[0].size
        for row in rows_list:
            if self.columns_amount != row.size:
                raise ValueError("All Matrix rows must be of the same length")


class Row:
    def __init__(self, values_list):
        self.values_list = values_list
        self.type = analyze_types(values_list)
        if self.type is None:
            raise ValueError("Row values must be of compatible types")
        self.size = len(values_list)

    def getSize(self):
        return self.size

    def getFirst(self):
        return self.values_list[0]

    def getSecond(self):
        return self.values_list[1]


def analyze_types(of):
    universal_type = of[0].type
    for element in of:
        if not types_equivalent(element.type, universal_type):
            return None
        universal_type = max(universal_type, element.type)
    return universal_type


class Vector:
    def __init__(self, value=None, vec=None):
        self.value = list()
        if value is not None:
            self.value.append(value)

        if vec is not None:
            if type(vec) is Vector:
                self.value += vec.value
            else:
                raise ValueError("Wrong value passed to Vector - should be {0}, not {1}".format(type(vec), Vector))

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]


class Function:
    def __init__(self, name, argument):  # returnType):
        if not types_strong_equivalent(argument.type, Types.INT):
            raise ValueError("The argument of {} must be an INT".format(name))  # TODO upper impl
        self.name = name
        self.arguments = argument
        self.type = Types.INT
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
        if operator == Operator.TRANSPOSE and element.is_matrix == 0:
            raise ValueError("Transposition operator used with invalid type {}".format(Types.typeName(element.type)))
        self.element = element
        self.operator = operator
        self.type = element.type
        self.is_matrix = element.is_matrix


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
        self.is_matrix = left.is_matrix


class LogicalExpression:
    def __init__(self, left, right, operator):
        if not types_equivalent(left.type, right.type):
            raise ValueError("Cannot compare {} with {}".format(left.type, right.type))
        self.left = left
        self.right = right
        self.operator = operator


class Assignment:  # TODO check complex type
    def __init__(self, left, right, operator):
        if not types_equivalent(left.type, right.type):
            raise ValueError("Cannot use {} for {} and {}".format(operator,
                                                                  Types.typeName(left.type),
                                                                  Types.typeName(right.type)))

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
