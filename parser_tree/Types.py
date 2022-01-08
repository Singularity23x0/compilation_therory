import copy


class Type:
    def __init__(self, core_type):
        self.core_type = core_type

    def __eq__(self, other):
        return self.structure_equivalent(other) and self.core_type == other.core_type

    def structure_equivalent(self, other):
        return self.__class__ == other.__class__

    def get_size(self):
        pass

    def update_core_type(self, to):
        self.core_type = to

    def __str__(self):
        return self.__class__.__name__ + self.details()

    def details(self):
        return CoreTypes.type_name(self.core_type)

    def copy_with_type(self, new_type):
        cp = copy.deepcopy(self)
        cp.core_type = new_type
        return cp

    def comparable_with(self, comparison_operator):
        return True


class GenericType(Type):
    pass


class MatrixType(Type):
    def __init__(self, core_type, rows, cols):
        super().__init__(core_type)
        self.rows = rows
        self.cols = cols

    def structure_equivalent(self, other):
        return super().structure_equivalent(other) and \
               compare_sizes(self.cols, other.cols) and \
               compare_sizes(self.rows, other.rows)

    def get_size(self):
        return self.rows, self.cols

    def details(self):
        return CoreTypes.type_name(self.core_type) + " " + str(self.rows) + "x" + str(self.cols)

    def comparable_with(self, comparison_operator):
        return comparison_operator == "=="


class RowType(Type):
    def __init__(self, core_type, size):
        super().__init__(core_type)
        self.size = size

    def structure_equivalent(self, other):
        return super().structure_equivalent(other) and compare_sizes(self.size, other.size)

    def get_size(self):
        return self.size

    def details(self):
        return CoreTypes.type_name(self.core_type) + " " + str(self.size)

    def comparable_with(self, comparison_operator):
        return comparison_operator == "=="


class CoreTypes:
    INT = 1
    FLOAT = 2
    STRING = 3
    T = ["INT", "FLOAT", "STRING"]

    def type_name(i):
        return CoreTypes.T[i - 1]


def compare_sizes(size1, size2):
    return size1 is None or size2 is None or size1 == size2


def core_types_compatible(core_type1, core_type2):
    return core_type1 == core_type2 or (core_type1 <= 2 and core_type2 <= 2)


def is_matrix(obj):
    return isinstance(obj, MatrixType)


def equivalent(type1, type2):
    if type1 is None or type2 is None:
        return False
    return type1.structure_equivalent(type2) and \
           type2.structure_equivalent(type1) and \
           core_types_compatible(type1.core_type, type2.core_type)


def equal(type1, type2):
    if type1 is None or type2 is None:
        return False
    return type1 == type2


if __name__ == "__main__":
    pass
