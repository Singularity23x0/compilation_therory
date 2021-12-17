import parser_tree.Types as Types
import parser_tree.structure as struct


class TypeDef:
    def __init__(self):
        pass

    def get_type(operator, el1, el2=None):
        if el2 is None:
            return get_type_unary(operator, el1)
        return get_type_binary(operator, el1, el2)


def get_type_binary(operator, el1, el2):
    if operator == "=":
        return el2
    if operator == struct.Operator.MSTAR:
        if not Types.is_matrix(el1) or not Types.is_matrix(el2):
            return None
        if Types.core_types_compatible(el1.core_type, el2.core_type):
            if el1.core_type==Types.CoreTypes.STRING:
                return None
            else:
                if el1.cols==el2.rows:
                    return Types.MatrixType(max(el1.core_type, el2.core_type),el2.rows,el1.cols)
                else:
                    return None
        else:
            return None
    if not Types.equivalent(el1, el2):
        return None
    if (operator in {"+=", "-=", "*=", "/="} or operator <= 4) and Types.is_matrix(el1):
        return None
    if not isinstance(operator,str) and 5 <= operator <= 8 and not Types.is_matrix(el1):
        return None
    if not isinstance(operator,str) and operator >= 9:
        return None
    if (el1.core_type==Types.CoreTypes.STRING or el2.core_type==Types.CoreTypes.STRING )\
            and (not (operator == "=" or operator == "+=" or operator == 1) or el1.core_type!=el2.core_type):
        return None
    el1.core_type = max(el1.core_type, el2.core_type)
    return el1


def get_type_unary(operator, el):
    if el is None:
        return None
    if el.core_type == Types.CoreTypes.STRING:
        return None
    if operator == struct.Operator.TRANSPOSE and Types.is_matrix(el):
        return Types.MatrixType(el.core_type, el.cols, el.rows)
    if operator == struct.Operator.UMINUS:
        return el
    return None


if __name__ == '__main__':
    pass
