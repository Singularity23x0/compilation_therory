from TreeART import *
import traceback


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    def __init__(self, name):
        self.name = name

    def addHead(f, shift, last, name,end="\n"):
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
        f.write(line.encode("utf8"))

    def draw(self, root):
        f = open(self.name, "wb")
        try:
            root.write(f, [], True)
        except AttributeError:
            print(traceback.format_exc())
        # f.write(x.encode("utf8"))
        # f.write("\n".encode("utf8"))

        f.close()

    @addToClass(Block)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "BLOCK")
        self.segment.write(f, shift+[last], True)

    @addToClass(Segment)
    def write(self, f, shift, last):
        i = 0
        for instruction in self.instructionList:
            i += 1
            instruction.write(f, shift, i == len(self.instructionList))

    @addToClass(Assignment)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, self.operator)
        self.left.write(f,shift+[last],False)
        self.right.write(f,shift+[last],True)


    @addToClass(If)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "IF")
        self.condition.write(f,shift+[last],False)
        self.inside.write(f, shift + [last], True)

    @addToClass(IfElse)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "IFELSE")
        self.condition.write(f, shift + [last], False)
        self.inside.write(f, shift + [last], False)
        self.insideElse.write(f, shift + [last], True)

    @addToClass(While)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "WHILE")
        self.condition.write(f, shift + [last], False)
        self.inside.write(f, shift + [last], True)

    @addToClass(For)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "For variable: "+self.idv.name)
        self.rangeS.write(f,shift+[last],False)
        self.inside.write(f, shift + [last], True)

    @addToClass(Variable)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "Variable")
        TreePrinter.addHead(f, shift+[last], False, "Name: " + self.name)
        TreePrinter.addHead(f, shift+[last], True, "type: " + Types.typeName(self.typeV))

    @addToClass(Value)
    def write(self, f, shift, last):
        if self.const and self.typeV != Types.MATRIX:
            TreePrinter.addHead(f, shift, last, "SINGLE_VALUE: CONST"+" type: "+Types.typeName(self.typeV)+" value: "+str(self.value))
        else:
            l="SINGLE_VALUE:"
            if self.const:
                l+=" CONST"
            TreePrinter.addHead(f, shift, last,l + " type: " + Types.typeName(self.typeV) + " ")
            self.value.write(f,shift+[last],True)

    @addToClass(Function)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "FUNCTION name: " + self.name)
        self.arguments.write(f,shift+[last],True)

    @addToClass(ArithmeticExpressionBinary)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, Operator.operatorName(self.operator))
        self.left.write(f, shift + [last], False)
        self.right.write(f, shift + [last], True)

    @addToClass(LogicalExpression)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, self.operator)
        self.left.write(f, shift + [last], False)
        self.right.write(f, shift + [last], True)

    @addToClass(ArithmeticExpressionUnary)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, Operator.operatorName(self.operator))
        self.element.write(f, shift + [last], True)

    @addToClass(Matrix)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "MATRIX type: "+ Types.typeName(self.type) +" size:"+str(self.rowSize)+"x"+str(self.columnNum))
        i = 0
        for instruction in self.rowList:
            i += 1
            instruction.write(f, shift+[last], i == len(self.rowList))

    @addToClass(Row)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last,"ROW")
        self.valueList.write(f,shift+[last],True)

    @addToClass(Vector)
    def write(self, f, shift, last):
        i = 0
        for instruction in self.value:
            i += 1
            instruction.write(f, shift, i == len(self.value))

    @addToClass(Print)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "PRINT")
        self.vector.write(f,shift+[last],True)

    @addToClass(Range)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "RANGE")
        self.fro.write(f,shift+[last],False)
        self.to.write(f, shift + [last], True)

    @addToClass(Empty)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "EMPTY")

    @addToClass(Break)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "BREAK")

    @addToClass(Cont)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "CONT")

    @addToClass(SelectionSingle)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "SINGLE_FROM_MATRIX")
        self.matrix.write(f,shift+[last],False)
        self.pos1.write(f,shift+[last],False)
        self.pos2.write(f,shift+[last],True)

    @addToClass(SelectColumn)
    def write(self, f, shift, last):
        TreePrinter.addHead(f, shift, last, "ROW_FROM_MATRIX")
        self.matrix.write(f, shift + [last], False)
        self.pos.write(f, shift + [last], True)





