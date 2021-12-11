import Types
import structure as struct


class TypeDef:
    def __init__(self):
        pass

    def get_type(self, operator, el1, el2=None):
        if el2 is not None:
            return get_type_binary(operator, el1, el2)
        return get_type_unary(operator, el1)


def get_type_binary(operator, el1, el2):
    if not Types.equivalent(el1, el2):
        return None
    if 5 <= operator <= 8 and not Types.is_matrix(el1):
        return None
    el1.core_type = max(el1.core_type, el2.core_type)
    return el1


def get_type_unary(operator, el):
    if operator == struct.Operator.TRANSPOSE and Types.is_matrix(el):
        return Types.MatrixType(el.core_type, el.cols, el.rows)
    if operator == struct.Operator.UMINUS:
        return el
    return None
