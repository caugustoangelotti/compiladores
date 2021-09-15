from lexico import lexer
from lexico import token
import sys

class Sintatico:
    def __init__(self, _charsArray):
        self.lexico = lexer.Lexico(_charsArray)
        self.currentSimbol = ""
    
    def getNewSimbol(self):
        tkn = self.lexico.nexToken()
        self.currentSimbol = tkn.getTokenType()
        return self.currentSimbol

    def programa(self):
        if(self.currentSimbol == "program"):
            self.getNewSimbol()
            if(self.currentSimbol() == "ident"):
                self.corpo()
                if(self.currentSimbol == "."):
                    return "tudo certo"
                else:
                    raise Exception("Erro sintatico esperado .")
                    exit()
            else:
                raise Exception("Erro sintatico esperado ident")
                exit()
        else:
            raise Exception("Erro sintatico esperando program")
            exit()
    def corpo(self):
        self.getNewSimbol()
        self.dc()
        if(self.currentSimbol == "begin"):
            self.comandos()
            if(self.currentSimbol == "end"):
                self.getNewSimbol()
            else:
                raise Exception("Erro sintatico esperado end")
                exit()
        else:
            raise Exception("Erro sintatico esperado begin")
            exit()

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