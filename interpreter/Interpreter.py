import math
from typing import Union

import parser_tree.structure as struc
from parser_tree import SymbolTable
from interpreter.Memory import *
from interpreter.Exceptions import *
from interpreter.visit import *
import sys

sys.setrecursionlimit(10000)


def compare_sizes(mtx1, mtx2, operator):
    if isinstance(mtx1, struc.Matrix):
        if operator == 3:
            if mtx1.columns_amount != mtx2.rows_amount:
                raise ValueError("Incompatible sizes for matrix multiplication")
        else:
            if mtx1.columns_amount != mtx2.columns_amount or mtx1.rows_amount != mtx2.rows_amount:
                raise ValueError("Incompatible sizes for matrix operation - {}x{} and {}x{}"
                                 .format(mtx1.rows_amount, mtx1.columns_amount, mtx2.rows_amount, mtx2.columns_amount))


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
        except BaseException as err:
            if node.prime:
                return str(err)
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
        if isinstance(node.value, (int, float, str)):
            return node.value
        return self.visit(node.value)

    @when(struc.Variable)
    def visit(self, node):
        return self.memory.get(node.name)

    def evalSelectSingle(self, node):
        m = self.visit(node.matrix)
        p1 = self.visit(node.pos1)
        p2 = self.visit(node.pos2)
        horizontal_size = m.columns_amount
        vertical_size = m.rows_amount
        if p1 < 0 or p1 > vertical_size:
            raise IndexOutOfBounds(p1, 0, vertical_size)
        if p2 < 0 or p2 > horizontal_size:
            raise IndexOutOfBounds(p2, 0, horizontal_size)
        return m, p1, p2

    @when(struc.SelectionSingle)
    def visit(self, node):
        m, p1, p2 = Interpreter.evalSelectSingle(self, node)
        return m.rows_list[p1].values_list[p2]

    def evalSelectRow(self, node):
        m = self.visit(node.matrix)
        p = self.visit(node.pos)
        vertical_size = m.rows_amount
        if p < 0 or p > vertical_size:
            raise IndexOutOfBounds(p, 0, vertical_size)
        return m, p

    @when(struc.SelectRow)
    def visit(self, node):
        m, p = Interpreter.evalSelectRow(self, node)
        return m.rows_list[p]

    @when(struc.Matrix)
    def visit(self, node):
        for i in range(node.rows_amount):
            node.rows_list[i] = self.visit(node.rows_list[i])
        typ = node.rows_list[0].typ
        if typ == int:
            for i in range(1, node.rows_amount):
                if node.rows_list[i].typ == float:
                    typ = float
        node.type = typ
        return node

    @when(struc.Row)
    def visit(self, node):
        for i in range(node.size):
            node.values_list[i] = self.visit(node.values_list[i])
        typ = type(node.values_list[0])
        if typ == int:
            for i in range(1, node.size):
                if isinstance(node.values_list[i], float):
                    typ = float
        node.typ = typ
        return node

    @when(struc.Vector)
    def visit(self, node):
        print("debugging alert")

    @when(struc.Function)
    def visit(self, node):
        argument = self.visit(node.arguments)
        if argument <= 0 or not isinstance(argument, int):
            raise ValueError("Invalid function argument " + str(argument))

        def make_zero(arg):
            return struc.Matrix.makeEmpty(arg, arg)

        def make_ones(arg):
            return struc.Matrix.makeEmpty(arg, arg, 1)

        def make_eye(arg):
            m = struc.Matrix.makeEmpty(arg, arg)
            for i in range(arg):
                m.rows_list[i].values_list[i] = 1
            return m

        T = {"eye": make_eye, "ones": make_ones, "zeros": make_zero}
        return T[node.name](argument)

    class Arithmetic:
        def add(el1, el2):
            return el1 + el2

        def sub(el1, el2):
            return el1 - el2

        def mul(el1, el2):
            return el1 * el2

        def div(el1, el2):
            return el1 / el2

        def mmul(el1, el2):
            return struc.Matrix.mmul(el1, el2)

        def mdiv(el1, el2):
            return struc.Matrix.mdiv(el1, el2)

        Operators = [0, add, sub, mul, div, add, sub, mmul, mdiv]

        def calculate(el1, el2, operator):
            compare_sizes(el1, el2, operator)  # 7 8
            return Interpreter.Arithmetic.Operators[operator](el1, el2)

    @when(struc.ArithmeticExpressionBinary)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Interpreter.Arithmetic.calculate(left, right, node.operator)

    @when(struc.ArithmeticExpressionUnary)
    def visit(self, node):
        if node.operator == struc.Operator.TRANSPOSE:
            return self.visit(node.element).transpose()
        else:
            return -self.visit(node.element)

    class Comparator:
        def le(el1, el2):
            return el1 <= el2

        def ge(el1, el2):
            return el1 >= el2

        def eq(el1, el2):
            return el1 == el2

        def ne(el1, el2):
            return el1 != el2

        def lt(el1, el2):
            return el1 < el2

        def gt(el1, el2):
            return el1 > el2

        Operators = {"<=": le, ">=": ge, "==": eq, "!=": ne, "<": lt, ">": gt}

        def compare(el1, el2, operator):
            return Interpreter.Comparator.Operators[operator](el1, el2)

    @when(struc.LogicalExpression)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Interpreter.Comparator.compare(left, right, node.operator)

    class Assignmenter:
        def makeVariable(interpreter, el1, el2):
            interpreter.memory.insert(el1.name, el2)

        def assigm(interpreter, el1, el2):
            interpreter.memory.insert(el1.name, el2)

        def adda(interpreter, el1, el2):
            interpreter.memory.insert(el1.name, interpreter.visit(el1) + el2)

        def suba(interpreter, el1, el2):
            interpreter.memory.insert(el1.name, interpreter.visit(el1) - el2)

        def mula(interpreter, el1, el2):
            interpreter.memory.insert(el1.name, interpreter.visit(el1) * el2)

        def diva(interpreter, el1, el2):
            interpreter.memory.insert(el1.name, interpreter.visit(el1) / el2)

        def assigmS(interpreter, el1, el2):
            m, p1, p2 = interpreter.evalSelectSingle(el1)
            m.setSingle(p1, p2, el2)

        def addaS(interpreter, el1, el2):
            m, p1, p2 = interpreter.evalSelectSingle(el1)
            m.setSingle(p1, p2, m.rows_list[p1].values_list[p2] + el2)

        def subaS(interpreter, el1, el2):
            m, p1, p2 = interpreter.evalSelectSingle(el1)
            m.setSingle(p1, p2, m.rows_list[p1].values_list[p2] - el2)

        def mulaS(interpreter, el1, el2):
            m, p1, p2 = interpreter.evalSelectSingle(el1)
            m.setSingle(p1, p2, m.rows_list[p1].values_list[p2] * el2)

        def divaS(interpreter, el1, el2):
            m, p1, p2 = interpreter.evalSelectSingle(el1)
            m.setSingle(p1, p2, m.rows_list[p1].values_list[p2] / el2)

        def assigmR(interpreter, el1, el2):
            m, p = interpreter.evalSelectRow(el1)
            m.setRow(p, el2)

        def addaR(interpreter, el1, el2):
            m, p = interpreter.evalSelectRow(el1)
            m.setRow(p, m.rows_list[p] + el2)

        def subaR(interpreter, el1, el2):
            m, p = interpreter.evalSelectRow(el1)
            m.setRow(p, m.rows_list[p] - el2)

        def mulaR(interpreter, el1, el2):
            m, p = interpreter.evalSelectRow(el1)
            m.setRow(p, m.rows_list[p] * el2)

        def divaR(interpreter, el1, el2):
            m, p = interpreter.evalSelectRow(el1)
            m.setRow(p, m.rows_list[p] / el2)

        OperatorsNormal = {"=": assigm, "+=": adda, "-=": suba, "*=": mula, "/=": diva}
        OperatorsSelectSingle = {"=": assigmS, "+=": addaS, "-=": subaS, "*=": mulaS, "/=": divaS}
        OperatorsSelectRow = {"=": assigmR, "+=": addaR, "-=": subaR, "*=": mulaR, "/=": divaR}
        T = {struc.Variable: OperatorsNormal, struc.SelectionSingle: OperatorsSelectSingle,
             struc.SelectRow: OperatorsSelectRow}

        def assi(interpreter, el1, el2, operator):
            el2 = interpreter.visit(el2)
            if operator == "=" and isinstance(el1, struc.Variable) and not interpreter.memory.has(el1.name):
                Interpreter.Assignmenter.makeVariable(interpreter, el1, el2)
            else:
                Interpreter.Assignmenter.T[type(el1)][operator](interpreter, el1, el2)

    @when(struc.Assignment)
    def visit(self, node):
        Interpreter.Assignmenter.assi(self,node.left,node.right,node.operator)

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
