from auxiliares import typeConstants

class Token:
    def __init__(self, tipo, valor = None):
        return

    def __repr__(self):
        if self.valor: return f"Tipo = {self.tipo} Valor = {self.valor}"
        return f"Tipo = {self.tipo}"