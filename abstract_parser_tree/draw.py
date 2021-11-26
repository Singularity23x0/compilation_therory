import traceback
from abstract_parser_tree.structure import *


def add_to_class(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    def __init__(self, name):
        self.name = name

    def add_head(self, shift, last, name, end="\n"):
        line = ""
        if shift:
            for i in shift:
                if not i:
                    line += "║ "
                else:
                    line += "  "
            if last:
                line += "╚>"
            else:
                line += "╠>"
        line += name + end
        self.write(line.encode("utf8"))

    def draw(self, root):
        f = open(self.name, "wb")
        try:
            root.write(f, [], True)
        except AttributeError:
            print(traceback.format_exc())
        # f.write(x.encode("utf8"))
        # f.write("\n".encode("utf8"))

        f.close()

    @add_to_class(Block)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "BLOCK")
        self.segment.write(f, shift + [last], True)

    @add_to_class(Segment)
    def write(self, f, shift, last):
        i = 0
        for instruction in self.instructionList:
            i += 1
            instruction.write(f, shift, i == len(self.instructionList))

    @add_to_class(Assignment)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, self.operator)
        self.left.write(f, shift + [last], False)
        self.right.write(f, shift + [last], True)

    @add_to_class(If)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "IF")
        self.condition.write(f, shift + [last], False)
        self.inside.write(f, shift + [last], True)

    @add_to_class(IfElse)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "IFELSE")
        self.condition.write(f, shift + [last], False)
        self.inside.write(f, shift + [last], False)
        self.insideElse.write(f, shift + [last], True)

    @add_to_class(While)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "WHILE")
        self.condition.write(f, shift + [last], False)
        self.inside.write(f, shift + [last], True)

    @add_to_class(For)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "For variable: " + self.idv.name)
        self.rangeS.write(f, shift + [last], False)
        self.inside.write(f, shift + [last], True)

    @add_to_class(Variable)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "Variable")
        TreePrinter.add_head(f, shift + [last], False, "Name: " + self.name)
        TreePrinter.add_head(f, shift + [last], True, "type: " + Types.typeName(self.type))

    @add_to_class(Value)
    def write(self, f, shift, last):
        if self.const and self.type != Types.MATRIX:
            TreePrinter.add_head(f, shift, last,
                                 "SINGLE_VALUE: CONST," + " type: " + Types.typeName(self.type) + ", value: " + str(
                                     self.value))
        else:
            l = "SINGLE_VALUE:"
            if self.const:
                l += " CONST"
            TreePrinter.add_head(f, shift, last, l + " type: " + Types.typeName(self.type) + " ")
            self.value.write(f, shift + [last], True)

    @add_to_class(Function)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "FUNCTION name: " + self.name)
        self.arguments.write(f,shift+[last],True)

    @add_to_class(ArithmeticExpressionBinary)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, Operator.operator_name(self.operator))
        self.left.write(f, shift + [last], False)
        self.right.write(f, shift + [last], True)

    @add_to_class(LogicalExpression)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, self.operator)
        self.left.write(f, shift + [last], False)
        self.right.write(f, shift + [last], True)

    @add_to_class(ArithmeticExpressionUnary)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, Operator.operator_name(self.operator))
        self.element.write(f, shift + [last], True)

    @add_to_class(Matrix)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last,
                             "MATRIX type: " + Types.typeName(self.type) + " size:" + str(self.row_size) + "x" + str(
                                 self.columns_amount))
        i = 0
        for instruction in self.rows_list:
            i += 1
            instruction.write(f, shift + [last], i == len(self.rows_list))

    @add_to_class(Row)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "ROW")
        self.values_list.write(f, shift + [last], True)

    @add_to_class(Vector)
    def write(self, f, shift, last):
        i = 0
        for instruction in self.value:
            i += 1
            instruction.write(f, shift, i == len(self.value))

    @add_to_class(Print)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "PRINT")
        self.vector.write(f, shift + [last], True)

    @add_to_class(Return)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "Return")
        if self.value:
            self.value.write(f, shift + [last], True)

    @add_to_class(Range)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "RANGE")
        self.fro.write(f, shift + [last], last)
        self.to.write(f, shift + [last], last)

    @add_to_class(Empty)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "EMPTY")

    @add_to_class(Break)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "BREAK")

    @add_to_class(Cont)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "CONT")

    @add_to_class(SelectionSingle)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "SINGLE_FROM_MATRIX")
        self.matrix.write(f, shift + [last], False)
        self.pos1.write(f, shift + [last], False)
        self.pos2.write(f, shift + [last], True)

    @add_to_class(SelectColumn)
    def write(self, f, shift, last):
        TreePrinter.add_head(f, shift, last, "ROW_FROM_MATRIX")
        self.matrix.write(f, shift + [last], False)
        self.pos.write(f, shift + [last], True)
