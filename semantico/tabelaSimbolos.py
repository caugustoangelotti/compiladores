class TabelaSimbolos:
    def __init__(self) -> None:
        self.symbolTable = dict()
    
    def addSymbol(self, _key, _value):
        if self.containsKey(_key):
            return False
        self.symbolTable[_key] = _value
        return True
    
    def getSymbol(self, _key):
        if _key in self.symbolTable.keys():
            return self.symbolTable[_key]
        return None
    
    def containsKey(self, _key):
        if _key in self.symbolTable.keys():
            return True
        return False