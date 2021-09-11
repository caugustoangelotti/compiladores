class Token:
    def __init__(self, _tipo, _valor = None) -> None:
        self.tipo = _tipo
        self.valor = _valor
    
    def __repr__(self) -> str:
        return f"tkn = [{self.tipo}->{self.valor}]"