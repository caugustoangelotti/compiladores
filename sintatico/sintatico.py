from lexico import lexer
from auxiliares import reservedDic as reserved

class Sintatico:
    def __init__(self, _charsArray):
        self.lexico = lexer.Lexico(_charsArray)
        self.currentSimbol = ""
    
    def getNewSimbol(self):
        tkn = self.lexico.nexToken()
        self.currentSimbol = tkn.getTokenType()
        return self.currentSimbol

    def programa(self):
        if(self.currentSimbol == reserved.words['program']):
            self.getNewSimbol()
            if(self.currentSimbol() == reserved.tokenTypes['ident']):
                self.corpo()
                if(self.currentSimbol == reserved.literais['ponto']):
                    return "tudo certo"
                else:
                    raise Exception("Erro sintatico esperado .")
            else:
                raise Exception("Erro sintatico esperado ident")
        else:
            raise Exception("Erro sintatico esperando program")
    def corpo(self):
        self.getNewSimbol()
        self.dc()
        if(self.currentSimbol == reserved.words['begin']):
            self.comandos()
            if(self.currentSimbol == reserved.words['end']):
                self.getNewSimbol()
            else:
                raise Exception("Erro sintatico esperado end")
        else:
            raise Exception("Erro sintatico esperado begin")

    def dc(self):
        self.getNewSimbol()
        if self.currentSimbol in reserved.tipos.values():
            self.dc_v()
            self.mais_dc()
        else:
            return ''

    def mais_dc(self):
        self.getNewSimbol()
        if self.currentSimbol == reserved.literais['ponto_e_virgula']:
            self.dc()
        else:
            return ''

    def comandos(self):
        self.comando()
        self.mais_comandos()

    def mais_comandos(self):
        self.getNewSimbol()
        if self.currentSimbol == reserved.literais['ponto_e_virgula']:
            self.comandos()
        else:
            return ''

    def dc_v(self):
        self.tipo_var()
        if self.currentSimbol == reserved.literais['dois_pontos']:
            self.variaveis()
        else:
            raise Exception("Erro sintatico esperando :")
    def tipo_var(self):
        if self.currentSimbol in reserved.tipos.values():
            self.getNewSimbol()
        else:
            raise Exception("Erro esperado real ou integer")
    def variaveis(self):
        self.getNewSimbol()
        if self.currentSimbol == reserved.tokenTypes['ident']:
            self.mais_var()
        else:
            raise Exception('Erro sintatico esperando ident')
    def mais_var(self):
        self.getNewSimbol()
        if self.currentSimbol == reserved.literais['virgula']:
            self.variaveis()
        else:
            return ''   
    def relacao(self):
        if self.currentSimbol in reserved.operadoresLogicos.values():
            self.getNewSimbol()
        else:
            raise Exception("Esperando um operador logico")
    def condicao(self):
        self.expressao()
        self.relacao()
        self.expressao()
    def comando(self):
        self.getNewSimbol()
        if self.currentSimbol == reserved.words['read'] or self.currentSimbol == reserved.words['write']:
            self.getNewSimbol()
            if self.currentSimbol == reserved.literais['abre_parenteses']:
                self.getNewSimbol()
                if self.currentSimbol == reserved.tokenTypes['ident']:
                    self.getNewSimbol()
                    if self.currentSimbol == reserved.literais['fecha_parenteses']:
                        self.getNewSimbol()
                    else:
                        raise Exception('Erro esperado )')
                else:
                    raise Exception('Erro esperado ident')
            else:
                raise Exception("Erro esperado (")
        elif self.currentSimbol == reserved.tokenTypes['ident']:
            self.getNewSimbol()
            if self.currentSimbol == reserved.atribuicao['atribuicao']:
                self.expressao()
            else:
                raise Exception('Erro esperado :=')
        elif self.currentSimbol == reserved.words['if']:
            self.condicao()
            if self.currentSimbol == reserved.words['then']:
                self.comandos()
                self.pfalsa()
                if self.currentSimbol == reserved.literais['dollar']:
                    self.getNewSimbol()
                else:
                    raise Exception('Erro esperado $')
            else:
                raise Exception('Erro esperado then')
        else:
            raise Exception('Erro esperando comando ou identificador')
                
    def expressao(self):
        self.termo()
        self.outros_termos()
    def termo(self):
        self.op_un()
        self.fator()
        self.mais_fatores()
    def op_un(self):
        if self.currentSimbol == reserved.matematicos['menos']:
            self.getNewSimbol()
        else:
            return ''
    def op_add(self):
        if self.currentSimbol == reserved.matematicos['menos'] or self.currentSimbol == reserved.matematicos['mais']:
            self.getNewSimbol()
        else:
            raise Exception('Erro esperado + ou -')
    def op_mul(self):
        if self.currentSimbol == reserved.matematicos['mult'] or self.currentSimbol == reserved.matematicos['div']:
            self.getNewSimbol()
        else:
            raise Exception('Erro esperado * ou /')
    def outros_termos(self):
        if self.currentSimbol == reserved.matematicos['menos'] or self.currentSimbol == reserved.matematicos['mais']:
            self.op_add()
            self.termo()
            self.outros_termos()
        else:
            return ''
    def mais_fatores(self):
        if self.currentSimbol == reserved.matematicos['mult'] or self.currentSimbol == reserved.matematicos['div']:
            self.op_mul()
            self.fator()
            self.mais_fatores()
    def fator(self):
        return
    def pfalsa(self):
        return