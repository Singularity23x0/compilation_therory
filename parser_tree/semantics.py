from SymbolTable import SymbolTable
from TypeDef import TypeDef
from Types import Type


class SemanticChecker:
    typeDef = TypeDef()

    def __init__(self):
        self.symbolTable = SymbolTable()
        self.loopDepth = 0
        self.errorList = []

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)

    # def visit_<classname> ...

    def visit_Segment(self, node):
        for x in node.instructionList:
            self.visit(x)

    def visit_Block(self, node):
        self.symbolTable.addScope()
        self.visit(node.segment)
        self.symbolTable.removeScope()

    def visit_For(self, node):
        self.symbolTable.addScope()
        self.loopDepth += 1
        self.visit(node.rangeS)
        if self.symbolTable.getSymbol(node.idv.name) is None:
            self.symbolTable.addSymbol(node.idv.name, Type(int))
        else:
            self.errorList.append("variable named " + node.id.name + " already declared, can not be used in for")
        self.visit(node.inside)
        self.loopDepth -= 1
        self.symbolTable.removeScope()

    def visit_Range(self, node):
        typeL = self.visit(node.fro)
        typeR = self.visit(node.to)
        if not types_strong_equivalent(typeL, int) or not types_strong_equivalent(typeR, int):
            self.errorList.append("wrong type in range structure")

    def visit_While(self, node):
        self.loopDepth += 1
        self.visit(node.condition)
        self.visit(node.inside)
        self.loopDepth -= 1

    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.inside)

    def visit_IfElse(self, node):
        self.visit(node.condition)
        self.visit(node.inside)
        self.visit(node.insideElse)

    def visit_Value(self, node):
        return Type(node.value)  # TODO adapt to "Types"

    def visit_Variable(self,node):
        return self.symbolTable.getSymbol(node.name)

    def visit_SelectionSingle(self,node):
        typeM=self.visit(node.matrix)
        typePos1 = self.visit(node.pos1)
        typePos2 = self.visit(node.pos2)
        if not isMatrix(typeM):
            self.errorList.append("cannot index not matrix")
        if not types_strong_equivalent(typePos1, int) or not types_strong_equivalent(typePos2, int):
            self.errorList.append("cannot index with no int type")
        if isinstance(node.pos1,Value) and node.pos1.value<0:
            self.errorList.append("cannot index with no negative numbers")
        if isinstance(node.pos2,Value) and node.pos2.value<0:
            self.errorList.append("cannot index with no negative numbers")
        sizeX,sizeY=getSize(typeM)
        if node.pos1.value>=sizeX and sizeX!=UNDEFINED:
            self.errorList.append("index out of range")
        if node.pos2.value>=sizeY and sizeY!=UNDEFINED:
            self.errorList.append("index out of range")
        return cellType(node.natrix)

    def visit_SelectRow(self,node):
        typeM = self.visit(node.matrix)
        typePos = self.visit(node.pos)
        if not isMatrix(typeM):
            self.errorList.append("cannot index not matrix")
        if not types_strong_equivalent(typePos, int):
            self.errorList.append("cannot index with no int type")
        if isinstance(node.pos,Value) and node.pos.value<0:
            self.errorList.append("cannot index with no negative numbers")
        sizeX, sizeY = getSize(typeM)
        if node.pos1.value >= sizeX and sizeX != UNDEFINED:
            self.errorList.append("index out of range")
        return rowType(node.natrix,sizeY)

    def visit_Matrix(self,node):
        typeM=-1
        size=-1
        for x in node.row_list:
            typeTmp=self.visit(x)
            if not typeM!=-1 or not types_strong_equivalent(typeM,typeTmp):
                self.errorList.append("types difference")
            if not size!=-1 or not types_strong_equivalent(size,typeTmp.getSize()):
                self.errorList.append("row size difference")
            typeM=typeTmp
            size=typeTmp.getSize()
        return Type(matrix,node.rows_amount,node.columns_amount)

    def visit_Row(self,node):
        typeM = -1
        for x in node.values_list:
            typeTmp = self.visit(x)
            if not typeM!=-1 or not types_strong_equivalent(typeM,typeTmp):
                self.errorList.append("types difference")
            typeM = typeTmp
        return Type(row,node.size)

    def visit_Vector(self,node):
        print("visiting vector") # for testing


