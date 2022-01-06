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
        return node.value

    @when(struc.Variable)
    def visit(self, node):
        return self.memory.get(node.name)

    @when(struc.SelectionSingle)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.SelectRow)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.Matrix)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.Row)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.Vector)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.Function)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.ArithmeticExpressionUnary)  # TODO finish
    def visit(self, node):
        pass

    @when(struc.LogicalExpression)  # TODO finish
    def visit(self, node):
        pass

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
