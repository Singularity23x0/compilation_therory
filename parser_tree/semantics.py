from SymbolTable import SymbolTable
from TypeDef import TypeDef,getType
from Types import equal,equivalent,is_matrix,RowType,Generic,CoreTypes,MatrixType
from structure import Variable,Value,Matrix


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
            self.symbolTable.addSymbol(node.idv.name, Generic(CoreTypes.INT))
        else:
            self.errorList.append("variable named " + node.id.name + " already declared, can not be used in for")
        self.visit(node.inside)
        self.loopDepth -= 1
        self.symbolTable.removeScope()

    def visit_Range(self, node):
        typeL = self.visit(node.fro)
        typeR = self.visit(node.to)
        if typeL == None and isinstance(node.fro,Variable):
            self.errorList.append("variable " + node.fro.name + " not declared")
        if typeR == None and isinstance(node.to,Variable):
            self.errorList.append("variable " + node.to.name + " not declared")
        if not equal(typeL, CoreTypes.INT) or not equal(typeR, CoreTypes.INT):
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
        if isinstance(node.value,Matrix):
            return self.visit(node)
        A={int:1,float:2,str:3} # move to Types
        return Generic(A[type(node.value)])

    def visit_Variable(self,node): # TODO check if declared variable
        return self.symbolTable.getSymbol(node.name)

    def visit_SelectionSingle(self,node):
        typeM=self.visit(node.matrix)
        typePos1 = self.visit(node.pos1)
        typePos2 = self.visit(node.pos2)
        if typeM is None and isinstance(node.matrix,Variable):
            self.errorList.append("variable " + node.matrix.name + " not declared")
        if typePos1 is None and isinstance(node.pos1,Variable):
            self.errorList.append("variable " + node.pos1.name + " not declared")
        if typePos2 is None and isinstance(node.pos2,Variable):
            self.errorList.append("variable " + node.pos2.name + " not declared")
        if not is_matrix(typeM):
            self.errorList.append("cannot index not matrix")
        if not equal(typePos1, CoreTypes.INT) or not equal(typePos2, CoreTypes.INT):
            self.errorList.append("cannot index with no int type")
        if isinstance(node.pos1,Value) and node.pos1.value<0:
            self.errorList.append("cannot index with no negative numbers")
        if isinstance(node.pos2,Value) and node.pos2.value<0:
            self.errorList.append("cannot index with no negative numbers")
        sizeX,sizeY=typeM.get_size()
        if node.pos1.value>=sizeX and sizeX is not None:
            self.errorList.append("index out of range")
        if node.pos2.value>=sizeY and sizeY is not None:
            self.errorList.append("index out of range")
        return Generic(node.natrix)

    def visit_SelectRow(self,node):
        typeM = self.visit(node.matrix)
        typePos = self.visit(node.pos)
        if typeM is None and isinstance(node.matrix,Variable):
            self.errorList.append("variable " + node.matrix.name + " not declared")
        if typePos is None and isinstance(node.pos,Variable):
            self.errorList.append("variable " + node.pos.name + " not declared")
        if not is_matrix(typeM):
            self.errorList.append("cannot index not matrix")
        if not equal(typePos, CoreTypes.INT):
            self.errorList.append("cannot index with no int type")
        if isinstance(node.pos,Value) and node.pos.value<0:
            self.errorList.append("cannot index with no negative numbers")
        sizeX, sizeY = typeM.get_size()
        if node.pos1.value >= sizeX and sizeX is not None:
            self.errorList.append("index out of range")
        return RowType(typeM,sizeY)

    def visit_Matrix(self,node):
        typeM=-1
        size=-1
        for x in node.row_list:
            typeTmp=self.visit(x)
            if not typeM!=-1 or not equal(typeM,typeTmp):
                self.errorList.append("types difference")
            if not size!=-1 or not equal(size,typeTmp.getSize()):
                self.errorList.append("row size difference")
            typeM=typeTmp
            size=typeTmp.get_size()
        return MatrixType(typeM,node.rows_amount,node.columns_amount)

    def visit_Row(self,node):
        typeM = -1
        for x in node.values_list:
            typeTmp = self.visit(x)
            if typeTmp is None and isinstance(x, Variable):
                self.errorList.append("variable " + x.name + " not declared")
            if not typeM!=-1 or not equal(typeM,typeTmp):
                self.errorList.append("types difference")
            typeM = typeTmp
        return RowType(typeM,node.size)

    def visit_Vector(self,node):
        print("visiting vector") # for testing

    def visit_Function(self,node):
        typeS=self.visit(node.arguments)
        if not equal(typeS,CoreTypes.INT):
            self.errorList.append("incorrect argument - wrong type")
        if isinstance(node.arguments,Value):
            if node.arguments.value<1:
                self.errorList.append("incorrect argument - wrong value")
            return MatrixType(CoreTypes.INT,node.arguments.value,node.arguments.value)
        return MatrixType(CoreTypes.INT, None, None)

    def visit_ArithmeticExpressionUnary(self,node):
        typeE=self.visit(node.element)
        if typeE is None and isinstance(node.element, Variable):
            self.errorList.append("variable " + node.element.name + " not declared")
        typeAll=getType(node.operator,typeE)
        if typeAll==None:
            self.errorList.append("incorrect type for operator")
        else:
            return typeAll

    def visit_ArithmeticExpressionBinary(self,node):
        typeE1 = self.visit(node.left)
        typeE2 = self.visit(node.right)
        if typeE1 is None and isinstance(node.left, Variable):
            self.errorList.append("variable " + node.left.name + " not declared")
        if typeE2 is None and isinstance(node.right, Variable):
            self.errorList.append("variable " + node.right.name + " not declared")
        typeAll = getType(node.operator, typeE1, typeE2)
        if typeAll == None:
            self.errorList.append("incorrect type for operator")
        else:
            return typeAll

    def visit_LogicalExpression(self,node):
        typeE1 = self.visit(node.left)
        typeE2 = self.visit(node.right)
        if not equivalent(typeE1,typeE2):
            self.errorList.append("can not compare different type")

    def visit_Assignment(self,node):
        typeE1 = self.visit(node.left)
        typeE2 = self.visit(node.right)
        if typeE1 is None and isinstance(node.left, Variable):
            self.errorList.append("variable " + node.left.name + " not declared")
        if typeE2 is None and isinstance(node.right, Variable):
            self.errorList.append("variable " + node.right.name + " not declared")
        typeAll = getType(node.operator, typeE1, typeE2)
        if typeE1 == None and isinstance(node.left,Variable):
            typeE1 = typeAll
            self.symbolTable.addSymbol(node.left.name,typeE1)
        if not equal(typeE1,typeAll):
            self.errorList.append("can not assign to different type")

    def visit_Print(self,node):
        for x in node.vector:
            typeTmp = self.visit(x)
            if typeTmp is None and isinstance(x, Variable):
                self.errorList.append("variable " + x.name + " not declared")

    def visit_Return(self,node):
        typeTmp = self.visit(node.value)
        if typeTmp is None and isinstance(node.value, Variable):
            self.errorList.append("variable " + node.value.name + " not declared")

    def visit_Break(self,node):
        if self.loopDepth==0:
            self.errorList.append("break outside loop")

    def visit_Cont(self,node):
        if self.loopDepth==0:
            self.errorList.append("continue outside loop")

    def visit_Empty(self,node):
        pass