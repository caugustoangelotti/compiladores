class Token:
    def __init__(self, _tipo, _valor = None) -> None:
        self.tipo = _tipo
        self.valor = _valor
    
    def __repr__(self) -> str:
        return f"[Tipo:[{self.tipo}] Valor:[{self.valor}]]"
    
    def getTokenType(self):
        return self.tipo
    
    def getTokenValue(self):
        return self.valor