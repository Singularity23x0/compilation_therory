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


class Value:
    def __init__(self, value, typeV,const=False):
        self.const=const
        self.value = value
        self.typeV = typeV


class Variable:
    def __init__(self, name, typeV=Types.UNDEFINED):
        self.name = name
        self.typeV = typeV


class SelectionSingle:
    def __init__(self, matrix, pos1, pos2):
        self.matrix = matrix
        self.pos1 = pos1
        self.pos2 = pos2


class SelectColumn:
    def __init__(self, matrix, pos):
        self.matrix = matrix
        self.pos = pos


class Matrix:
    def __init__(self, rowList):
        self.rowList = rowList
        self.type = Types.UNDEFINED  # TODO findIt
        self.rowSize = 0  # TODO calculate it
        self.columnNum = len(rowList)


class Row:
    def __init__(self, valueList):
        self.valueList = valueList
        self.type = Types.UNDEFINED  # TODO findIt
        self.size = len(valueList)

    def getSize(self):
        return self.size

    def getFirst(self):
        return self.valueList[0]

    def getSecond(self):
        return self.valueList[1]


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
    T=["PLUS",
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
        self.element = element
        self.operator = operator


class ArithmeticExpressionBinary:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator
        # self.reultType  # TODO


class LogicalExpression:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator


class Assignment:
    def __init__(self, left, right, operator):
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
