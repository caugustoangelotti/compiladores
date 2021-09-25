class Simbolo:
    def __init__(self, _varName, _varType) -> None:
        self.varName = _varName
        self.varType = _varType

    def __repr__(self) -> str:
        return f"@<varName: {self.varName} varType: {self.varType}>"

    def getVarName(self):
        return self.varName

    def getType(self):
        return self.varType