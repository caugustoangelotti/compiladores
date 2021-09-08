class Token:
    def __init__(self, _tipo, _valor = None):
        self.tipo = _tipo
        self.valor = _valor

    def __repr__(self):
        if self.valor: return f"[Tipo = {self.tipo} , Valor = {self.valor}]"
        return f"[Tipo = {self.tipo}]"