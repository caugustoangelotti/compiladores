from lexico import lexer
from auxiliares import reservedWordsDic as reservedWords

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
        self.getNewSimbol()
        if self.currentSimbol == 'real' or self.currentSimbol == 'integer':
            self.dc_v()
            self.mais_dc()
        else:
            return ''

    def mais_dc(self):
        self.getNewSimbol()
        if self.currentSimbol == ';':
            self.dc()
        else:
            return ''

    def comandos(self):
        self.comando()
        self.mais_comandos()

    def mais_comandos(self):
        self.getNewSimbol()
        if self.currentSimbol == ';':
            self.comandos()
        else:
            return ''

    def dc_v(self):
        self.tipo_var()
        if self.currentSimbol == ':':
            self.variaveis()
        else:
            raise Exception("Erro sintatico esperando :")
            exit()
    def tipo_var(self):
        #tabela de simbolos
        pass
    def variaveis(self):
        self.getNewSimbol()
        if self.currentSimbol == 'ident':
            self.mais_var()
        else:
            raise Exception('Erro sintatico esperando ident')
            exit()
    def mais_var(self):
        self.getNewSimbol()
        if self.currentSimbol == ',':
            self.variaveis()
        else:
            return ''   
    def relacao(self):
        if self.currentSimbol in reservedWords.relacoes:
            self.getNewSimbol()
        else:
            raise Exception("Esperando um operador logico")
            exit()
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