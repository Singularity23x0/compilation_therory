import copy


class Node:
    def __init__(self):
        self.line = None

    def set_line(self, line):
        self.line = line
        return self

    def get_line(self):
        return "Unknown line: " if self.line == 0 else "At line {}: ".format(self.line)


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
    def __init__(self, segment, prime=False):
        self.segment = segment
        self.prime = prime
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


def get_type(val):
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

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value


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
    Typ = {(str, str): str, (int, int): int, (int, float): float, (float, int): float}

    def __init__(self, rows_list, typ=None):
        self.rows_list = rows_list
        self.type = typ
        self.rows_amount = len(rows_list)
        self.columns_amount = rows_list[0].size

    def makeEmpty(rows, columns, value=0, typ=int):
        m = Matrix([Row([])])
        m.rows_amount = rows
        m.columns_amount = columns
        m.rows_list = []
        m.type = typ
        for x in range(rows):
            m.rows_list.append(Row.makeEmpty(columns, value, typ))
        return m

    def getTypeArthmetci(t1, t2):
        return Matrix.Typ[(t1, t2)]

    def setSingle(self, p1, p2, el):
        self.rows_list[p1].setSingle(p2, el)
        self.type = Matrix.getTypeArthmetci(self.type, type(el))

    def setRow(self, p, el):
        self.rows_list[p] = el
        self.type = Matrix.getTypeArthmetci(self.type, el.typ)

    def __le__(self, other):
        for row1, row2 in zip(self.rows_list, other.rows_list):
            if not row1 <= row2:
                return False
        return True

    def __ge__(self, other):
        for row1, row2 in zip(self.rows_list, other.rows_list):
            if not row1 >= row2:
                return False
        return True

    def __eq__(self, other):
        for row1, row2 in zip(self.rows_list, other.rows_list):
            if not row1 == row2:
                return False
        return True

    def __ne__(self, other):
        for row1, row2 in zip(self.rows_list, other.rows_list):
            if not row1 != row2:
                return False
        return True

    def __lt__(self, other):
        for row1, row2 in zip(self.rows_list, other.rows_list):
            if not row1 < row2:
                return False
        return True

    def __gt__(self, other):
        for row1, row2 in zip(self.rows_list, other.rows_list):
            if not row1 > row2:
                return False
        return True

    def __neg__(self):
        m = copy.deepcopy(self)
        for el in range(self.rows_amount):
            m.rows_list[el] = -m.rows_list[el]
        return m

    def __add__(self, other):
        m = copy.deepcopy(self)
        for x in range(other.rows_amount):
            m.rows_list[x] += other.rows_list[x]
        m.type = Matrix.getTypeArthmetci(self.type, other.type)
        return m

    def __iadd__(self, other):
        for x in other.rows_amount:
            self.rows_list[x] += other.rows_list[x]
        self.type = Matrix.getTypeArthmetci(self.type, other.type)
        return self

    def __sub__(self, other):
        m = copy.deepcopy(self)
        for x in range(other.rows_amount):
            m.rows_list[x] -= other.rows_list[x]
        m.type = Matrix.getTypeArthmetci(self.type, other.type)
        return m

    def __isub__(self, other):
        for x in other.rows_amount:
            self.rows_list[x] -= other.rows_list[x]
        self.type = Matrix.getTypeArthmetci(self.type, other.type)
        return self

    def mmul(self, other):
        m = copy.deepcopy(self)
        for x in range(other.rows_amount):
            Row.immul(m.rows_list[x], other.rows_list[x])
        m.type = Matrix.getTypeArthmetci(self.type, other.type)
        return m

    def immul(self, other):
        for x in other.rows_amount:
            Row.immul(self.rows_list[x], other.rows_list[x])
        self.type = Matrix.getTypeArthmetci(self.type, other.type)
        return self

    def mdiv(self, other):
        m = copy.deepcopy(self)
        for x in range(other.rows_amount):
            Row.imdiv(m.rows_list[x], other.rows_list[x])
        m.type = float
        return m

    def imdiv(self, other):
        for x in other.rows_amount:
            Row.imdiv(self.rows_list[x], other.rows_list[x])
        self.type = float
        return self

    def __mul__(self, other):
        m = Matrix.makeEmpty(self.rows_amount, other.columns_amount)
        for i in range(self.rows_amount):
            for j in range(other.columns_amount):
                for p in range(self.columns_amount):
                    m.rows_list[i].values_list[j] += \
                        self.rows_list[i].values_list[p] * other.rows_list[p].values_list[j]
        m.type = Matrix.getTypeArthmetci(self.type, other.type)
        return m

    def __imul__(self, other):
        m = Matrix.makeEmpty(self.rows_amount, other.columns_amount)
        for i in range(self.rows_amount):
            for j in range(other.columns_amount):
                for p in range(self.columns_amount):
                    m.rows_list[i].values_list[j] += \
                        self.rows_list[i].values_list[p] * other.rows_list[p].values_list[j]
        self.rows_list = m.rows_list
        self.type = Matrix.getTypeArthmetci(self.type, other.type)
        self.rows_amount = m.rows_amount
        self.columns_amount = m.columns_amount
        return self
        # return m

    def transpose(self):
        m = Matrix.makeEmpty(self.columns_amount, self.rows_amount)
        for i in range(self.columns_amount):
            for j in range(self.rows_amount):
                m.rows_list[i].values_list[j] = self.rows_list[j].values_list[i]
        return m

    def __str__(self):
        s = "<" + self.type.__name__ + ">:["
        for row in self.rows_list:
            s += str(row) + ','
        return s[:-1] + "]"


class Row(Node):
    Typ = {(str, str): str, (int, int): int, (int, float): float, (float, int): float}

    def __init__(self, values_list, typ=None):
        self.values_list = values_list
        self.size = len(values_list)
        self.typ = typ

    def getSize(self):
        return self.size

    def getFirst(self):
        return self.values_list[0]

    def getSecond(self):
        return self.values_list[1]

    def makeEmpty(columns, value=0, typ=int):
        return Row(Vector([value for x in range(columns)]), typ)

    def getTypeArthmetci(t1, t2):
        return Row.Typ[(t1, t2)]

    def setSingle(self, p, el):
        self.values_list[p] = el
        self.typ = Row.getTypeArthmetci(self.typ, type(el))

    def __le__(self, other):
        for val1, val2 in zip(self.values_list, other.values_list):
            if not val1 <= val2:
                return False
        return True

    def __ge__(self, other):
        for val1, val2 in zip(self.values_list, other.values_list):
            if not val1 >= val2:
                return False
        return True

    def __eq__(self, other):
        for val1, val2 in zip(self.values_list, other.values_list):
            if not val1 == val2:
                return False
        return True

    def __ne__(self, other):
        for val1, val2 in zip(self.values_list, other.values_list):
            if not val1 != val2:
                return False
        return True

    def __lt__(self, other):
        for val1, val2 in zip(self.values_list, other.values_list):
            if not val1 < val2:
                return False
        return True

    def __gt__(self, other):
        for val1, val2 in zip(self.values_list, other.values_list):
            if not val1 > val2:
                return False
        return True

    def __neg__(self):
        r = copy.deepcopy(self)
        for el in range(self.size):
            r.values_list[el] = -r.values_list[el]
        return r

    def __add__(self, other):
        r = copy.deepcopy(self)
        for x in range(other.size):
            r.values_list[x] += other.values_list[x]
        r.typ = Row.getTypeArthmetci(self.typ, other.typ)
        return r

    def __iadd__(self, other):
        for x in range(other.size):
            self.values_list[x] += other.values_list[x]
        self.typ = Row.getTypeArthmetci(self.typ, other.typ)
        return self

    def __sub__(self, other):
        r = copy.deepcopy(self)
        for x in range(other.size):
            r.values_list[x] -= other.values_list[x]
        r.typ = Row.getTypeArthmetci(self.typ, other.typ)
        return r

    def __isub__(self, other):
        for x in range(other.size):
            self.values_list[x] -= other.values_list[x]
        self.typ = Row.getTypeArthmetci(self.typ, other.typ)
        return self

    def mmul(self, other):
        r = copy.deepcopy(self)
        for x in range(other.size):
            r.values_list[x] *= other.values_list[x]
        r.typ = Row.getTypeArthmetci(self.typ, other.typ)
        return r

    def immul(self, other):
        for x in range(other.size):
            self.values_list[x] *= other.values_list[x]
        self.typ = Row.getTypeArthmetci(self.typ, other.typ)
        return self

    def mdiv(self, other):
        r = copy.deepcopy(self)
        for x in range(other.size):
            r.values_list[x] /= other.values_list[x]
        r.typ = float
        return r

    def imdiv(self, other):
        for x in range(other.size):
            self.values_list[x] /= other.values_list[x]
        self.typ = float
        return self

    def __str__(self):
        s = "["
        for val in self.values_list:
            s += str(val) + ','
        return s[:-1] + "]"


class Vector(Node):
    def __init__(self, value=None, vec=None):
        self.value = list()
        if value is not None:
            if isinstance(value, list):
                self.value += value
            else:
                self.value.append(value)

        if vec is not None:
            self.value += vec.value

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]

    def __setitem__(self, item, value):
        self.value[item] = value

    def __iter__(self):
        return self.value.__iter__()


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
