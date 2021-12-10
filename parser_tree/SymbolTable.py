class SymbolTable:
    def __init__(self):
        self.scopeList = []

    def addScope(self):
        self.scopeList.append(dict())

    def removeScope(self):
        self.scopeList.pop()

    def addSymbol(self, symbolName, symbolType):
        if self.getSymbol(symbolName) is None:
            self.scopeList[-1][symbolName] = symbolType

    def getSymbol(self, symbolName):  # return None if symbol not found
        for i in range(len(self.scopeList) - 1, -1, -1):
            if symbolName in self.scopeList[i]:
                return self.scopeList[i][symbolName]
        return None
