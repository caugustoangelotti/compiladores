from lexico import lexer
from lexico import token

class Sintatico:
    def __init__(self, _charsArray):
        self.lexico = lexer.Lexico(_charsArray)
        self.currentSimbol = ""
    
    def getNewSimbol(self):
        tkn = self.lexico.nexToken()
        self.currentSimbol = tkn.getTokenValue()
        return self.currentSimbol

    def programa(self):
        return
    def corpo(self):
        return
    def dc(self):
        return
    def mais_dc(self):
        return
    def comandos(self):
        return
    def mais_comandos(self):
        return
    def dc_v(self):
        return
    def tipo_var(self):
        return
    def variaveis(self):
        return
    def mais_var(self):
        return
    def dc_v(self):
        return
    def relacao(self):
        return
    def condicao(self):
        return
    def comando(self):
        return
    def expressao():
        return
    def termo(self):
        return
    def op_un(self):
        return
    def op_add(self):
        return
    def op_mul(self):
        return
    def outros_termos(self):
        return
    def mais_fatores(self):
        return
    def fator(self):
        return
    def pfalsa(self):
        return