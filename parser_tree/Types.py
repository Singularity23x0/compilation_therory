class Type:
    def __init__(self, core_type):
        self.core_type = core_type

    def __eq__(self, other):
        return self.structure_equivalent(other) and self.core_type == other.core_type

    def structure_equivalent(self, other):
        return self.__class__ == other.__class__


class Generic(Type):
    pass


class Matrix(Type):
    def __init__(self, core_type, rows, cols):
        super().__init__(core_type)
        self.rows = rows
        self.cols = cols

    def structure_equivalent(self, other):
        return super().structure_equivalent(other) and \
               compare_sizes(self.cols, other.cols) and \
               compare_sizes(self.rows, other.rows)


class Row(Type):
    def __init__(self, core_type, size):
        super().__init__(core_type)
        self.size = size

    def structure_equivalent(self, other):
        return super().structure_equivalent(other) and compare_sizes(self.size, other.size)


def compare_sizes(size1, size2):
    return size1 is None or size2 is None or size1 == size2


class CoreTypes:
    INT = 1
    FLOAT = 2
    STRING = 3
    COLUMN = 5
    T = ["INT", "FLOAT", "STRING", "COLUMN"]

    def type_name(i):
        return CoreTypes.T[i]


def core_types_compatible(core_type1, core_type2):
    return core_type1 == core_type2 or (core_type1 <= 2 and core_type2 <= 2)


def is_matrix(obj):
    return isinstance(obj, Matrix)


def equivalent(type1, type2):
    return type1.structure_equivalent(type2) and \
           type2.structure_equivalent(type1) and \
           core_types_compatible(type1.core_type, type2.core_type)


def equal(type1, type2):
    return type1 is type2


if __name__ == "__main__":
    pass
