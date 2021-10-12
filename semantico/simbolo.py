class Simbolo:
    def __init__(self, _varName, _varType, _enderecoRelativo = None) -> None:
        self.varName = _varName
        self.varType = _varType
        self.enderecoRelativo = _enderecoRelativo

    def __repr__(self) -> str:
        return f"@<varName: {self.varName} varType: {self.varType} enderecoRelativo: {self.enderecoRelativo}>"

    def getVarName(self):
        return self.varName

    def getType(self):
        return self.varType
    
    def getEnderecoRelativo(self):
        return self.enderecoRelativo