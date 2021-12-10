from SymbolTable import SymbolTable
from TypeDef import TypeDef


class SemanticChecker:
    typeDef = TypeDef()

    def __init__(self):
        self.symbolTable = SymbolTable()
        self.loopDepth = 0

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)

    # def visit_<classname> ...

