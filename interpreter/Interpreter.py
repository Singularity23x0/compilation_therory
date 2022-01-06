import parser_tree.structure as struc
from parser_tree import SymbolTable
from interpreter.Memory import *
from interpreter.Exceptions import *
from interpreter.visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter:
    def __init__(self):
        self.memory = MemoryStack(None)

    @on('node')
    def visit(self, node):
        pass

    @when(struc.Segment)
    def visit(self, node):
        for instruction in node.instructionList:
            self.visit(instruction)

    @when(struc.Block)
    def visit(self, node):
        self.memory.push(Memory("Block"))
        try:
            self.visit(node.segment)
        except ReturnException as err:
            if node.prime:
                return err.val
            else:
                raise err
        finally:
            self.memory.pop()

    @when(struc.For)
    def visit(self, node):
        begin, end = self.visit(node.rangeS)
        self.memory.push(Memory("For"))
        try:
            self.memory.insert(node.idv.name, 0)
            for i in range(begin, end + 1):
                self.memory.set(node.idv.name, i)
                try:
                    self.visit(node.inside)
                except BreakException:
                    break
                except ContinueException:
                    continue
        finally:
            self.memory.pop()

    @when(struc.Range)
    def visit(self, node):
        begin = self.visit(node.fro)
        end = self.visit(node.to)
        return begin, end

    @when(struc.While)
    def visit(self, node):
        while self.visit(node.condition):
            try:
                self.visit(node.inside)
            except BreakException:
                break
            except ContinueException:
                continue

    @when(struc.If)
    def visit(self, node):
        if self.visit(node.condition):
            self.visit(node.inside)

    @when(struc.IfElse)
    def visit(self, node):
        if self.visit(node.condition):
            self.visit(node.inside)
        else:
            self.visit(node.insideElse)

    @when(struc.Value)
    def visit(self, node):
        if isinstance(node.value,(int,float,str)):
            return node.value
        return self.visit(node.value)

    @when(struc.Variable)
    def visit(self, node):
        return self.memory.get(node.name)

    @when(struc.SelectionSingle)
    def visit(self, node, pointer=False):
        m = self.visit(node.matrix)
        p1 = self.visit(node.pos1)
        p2 = self.visit(node.pos2)
        if pointer:
            return m.rows_list[p1].values_list[p2]
        return m.rows_list[p1].values_list[p2].value

    @when(struc.SelectRow)
    def visit(self, node, pointer=False):
        m = self.visit(node.matrix)
        p = self.visit(node.pos)
        if pointer:
            return m, p
        return m.rows_list[p]

    @when(struc.Matrix)
    def visit(self, node):
        for i in range(node.rows_amount):
            node.rows_list[i] = self.visit(node.rows_list[i])
        typ = node.rows_list[0].typ
        if typ == int:
            for i in range(1, node.size):
                if node.values_list[0].typ == float:
                    typ = float
        node.typ = typ
        return node

    @when(struc.Row)
    def visit(self, node):
        for i in range(node.size):
            node.values_list[i] = self.visit(node.values_list[i])
        typ = type(node.values_list[0])
        if typ == int:
            for i in range(1, node.size):
                if isinstance(node.values_list[0], float):
                    typ = float
        node.typ = typ
        return node

    @when(struc.Vector)
    def visit(self, node):
        print("debugging alert")

    @when(struc.Function)
    def visit(self, node):
        argument = self.visit(node.arguments)

        def make_zero(arg):
            return struc.Matrix([struc.Row(struc.Vector([struc.Value(0) for y in range(arg)]), int)
                                 for x in range(arg)], int)

        def make_onse(arg):
            return struc.Matrix([struc.Row(struc.Vector([struc.Value(1) for y in range(arg)]), int)
                                 for x in range(arg)], int)

        def make_eye(arg):
            m = struc.Matrix([struc.Row(struc.Vector([struc.Value(0) for y in range(arg)]), int)
                              for x in range(arg)], int)
            for i in range(arg):
                m.rows_list[i].values_list[i].value = 1
            return m

        T = {"eye": make_zero, "ones": make_onse, "zeros": make_eye}
        return T[node.name](argument)

    @when(struc.ArithmeticExpressionBinary)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.ArithmeticExpressionUnary)  # TODO finish
    def visit(self, node):
        pass

    class Comparator:
        def le(el1, el2):
            return el1<=el2

        def ge(el1, el2):
            return el1>=el2

        def eq(el1, el2):
            return el1==el2

        def ne(el1, el2):
            return el1!=el2

        def lt(el1, el2):
            return el1<el2

        def gt(el1, el2):
            return el1>el2

        Operators = {"<=": le, ">=": ge, "==": eq, "!=": ne,"<": lt, ">": gt}

        def compare(el1, el2, operator):
            return Interpreter.Comparator.Operators[operator](el1, el2)

    @when(struc.LogicalExpression)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Interpreter.Comparator.compare(left,right,node.operator)

    @when(struc.Assignment)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.Print)
    def visit(self, node):
        i = len(node.vector)
        k = 0
        for val in node.vector:
            k += 1
            if i == k:
                print(self.visit(val), end="")
            else:
                print(self.visit(val), end=" ")

    @when(struc.Return)
    def visit(self, node):
        raise ReturnException(self.visit(node.value))

    @when(struc.Break)
    def visit(self, node):
        raise BreakException

    @when(struc.Cont)
    def visit(self, node):
        raise ContinueException()

    @when(struc.Empty)
    def visit(self, node):
        pass

    # @when(AST.BinOp)
    # def visit(self, node):
    #     r1 = node.left.accept(self)
    #     r2 = node.right.accept(self)
    #     # try sth smarter than:
    #     # if(node.op=='+') return r1+r2
    #     # elsif(node.op=='-') ...
    #     # but do not use python eval
    #
    # @when(AST.Assignment)
    # def visit(self, node):
    #     pass
    #
    # #
    #
    # # simplistic while loop interpretation
    # @when(AST.WhileInstr)
    # def visit(self, node):
    #     r = None
    #     while node.cond.accept(self):
    #         r = node.body.accept(self)
    #     return r
