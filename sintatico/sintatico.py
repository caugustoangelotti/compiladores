from lexico import lexer
from auxiliares import reservedDic as reserved

DEBUG = True

class Sintatico:
    def __init__(self, _charsArray):
        self.lexico = lexer.Lexico(_charsArray)
        self.currentSimbol = ""
    
    def getNewSimbol(self):
        tkn = self.lexico.nexToken()
        self.currentSimbol = tkn.getTokenType()
        if(DEBUG):
            tknValue = tkn.getTokenValue()
            print(f'type: {self.currentSimbol}  valor: {tknValue if tknValue != None else ""}')
        return self.currentSimbol

    def doSyntaxAnalise(self):
        try:
            self.getNewSimbol()
            if self.programa():
                print('Tudo certo')
        except RuntimeError as err:
            print(err)
            exit()


    def programa(self):
        if self.currentSimbol == reserved.words['program']:
            self.getNewSimbol()
            if self.currentSimbol == reserved.tokenTypes['ident']:
                self.getNewSimbol()
                self.corpo()
                if(self.currentSimbol == reserved.literais['ponto']):
                    return True
                else:
                    raise RuntimeError("Erro sintatico esperado .")
            else:
                raise RuntimeError("Erro sintatico esperado ident")
        else:
            raise RuntimeError("Erro sintatico esperando program")
    def corpo(self):
        self.dc()
        if(self.currentSimbol == reserved.words['begin']):
            self.getNewSimbol()
            self.comandos()
            if(self.currentSimbol == reserved.words['end']):
                self.getNewSimbol()
            else:
                raise RuntimeError("Erro sintatico esperado end")
        else:
            raise RuntimeError("Erro sintatico esperado begin")

    def dc(self):
        if self.currentSimbol in reserved.tipos.values():
            self.dc_v()
            self.mais_dc()
        else:
            return ''

    def mais_dc(self):
        if self.currentSimbol == reserved.literais['ponto_e_virgula']:
            self.getNewSimbol()
            self.dc()
        else:
            return ''

    def comandos(self):
        self.comando()
        self.mais_comandos()

    def mais_comandos(self):
        if self.currentSimbol == reserved.literais['ponto_e_virgula']:
            self.getNewSimbol()
            self.comandos()
        else:
            return ''

    def dc_v(self):
        self.tipo_var()
        if self.currentSimbol == reserved.literais['dois_pontos']:
            self.getNewSimbol()
            self.variaveis()
        else:
            raise RuntimeError("Erro sintatico esperando :")
    def tipo_var(self):
        if self.currentSimbol in reserved.tipos.values():
            self.getNewSimbol()
        else:
            raise RuntimeError("Erro esperado real ou integer")
    def variaveis(self):
        if self.currentSimbol == reserved.tokenTypes['ident']:
            self.getNewSimbol()
            self.mais_var()
        else:
            raise RuntimeError('Erro sintatico esperando ident')
    def mais_var(self):
        if self.currentSimbol == reserved.literais['virgula']:
            self.getNewSimbol()
            self.variaveis()
        else:
            return ''   
    def relacao(self):
        if self.currentSimbol in reserved.logicTokenTypes.values():
            self.getNewSimbol()
        else:
            raise RuntimeError("Esperando um operador logico")
    def condicao(self):
        self.expressao()
        self.relacao()
        self.expressao()
    def comando(self):
        if self.currentSimbol == reserved.words['read'] or self.currentSimbol == reserved.words['write']:
            self.getNewSimbol()
            if self.currentSimbol == reserved.literais['abre_parenteses']:
                self.getNewSimbol()
                self.variaveis()
                if self.currentSimbol == reserved.literais['fecha_parenteses']:
                    self.getNewSimbol()
                else:
                    raise RuntimeError('Erro esperado )')
            else:
                raise RuntimeError("Erro esperado (")
        elif self.currentSimbol == reserved.tokenTypes['ident']:
            self.getNewSimbol()
            if self.currentSimbol == reserved.tokenTypes['atribuicao']:
                self.getNewSimbol()
                self.expressao()
            else:
                raise RuntimeError('Erro esperado :=')
        elif self.currentSimbol == reserved.words['if']:
            self.getNewSimbol()
            self.condicao()
            if self.currentSimbol == reserved.words['then']:
                self.getNewSimbol()
                self.comandos()
                self.pfalsa()
                if self.currentSimbol == reserved.literais['dollar']:
                    self.getNewSimbol()
                else:
                    raise RuntimeError('Erro esperado $')
            else:
                raise RuntimeError('Erro esperado then')
        else:
            raise RuntimeError('Erro esperando comando ou identificador')
                
    def expressao(self):
        self.termo()
        self.outros_termos()
    def termo(self):
        self.op_un()
        self.fator()
        self.mais_fatores()
    def op_un(self):
        if self.currentSimbol == reserved.tokenTypes['subtracao']:
            self.getNewSimbol()
        else:
            return ''
    def op_add(self):
        if self.currentSimbol == reserved.tokenTypes['subtracao'] or self.currentSimbol == reserved.tokenTypes['adicao']:
            self.getNewSimbol()
        else:
            raise RuntimeError('Erro esperado + ou -')
    def op_mul(self):
        if self.currentSimbol == reserved.tokenTypes['multiplicacao'] or self.currentSimbol == reserved.tokenTypes['divisao']:
            self.getNewSimbol()
        else:
            raise RuntimeError('Erro esperado * ou /')

    def outros_termos(self):
        if self.currentSimbol == reserved.tokenTypes['subtracao'] or self.currentSimbol == reserved.tokenTypes['adicao']:
            self.op_add()
            self.termo()
            self.outros_termos()
        else:
            return ''

    def mais_fatores(self):
        if self.currentSimbol == reserved.tokenTypes['multiplicacao'] or self.currentSimbol == reserved.tokenTypes['divisao']:
            self.op_mul()
            self.fator()
            self.mais_fatores()
        else:
            return ''

    def fator(self):
        if self.currentSimbol == reserved.tokenTypes['ident'] or self.currentSimbol == reserved.tokenTypes['numero_int'] or self.currentSimbol == reserved.tokenTypes['numero_real']:
            self.getNewSimbol()
        elif self.currentSimbol == reserved.literais['abre_parenteses']:
            self.getNewSimbol()
            self.expressao()
            if self.currentSimbol == reserved.literais['fecha_parenteses']:
                self.getNewSimbol()
            else:
                raise RuntimeError('Erro esperado )')
        else:
            raise RuntimeError('Erro esperado variavel, numero: int ou real')

    def pfalsa(self):
        if self.currentSimbol == reserved.words['else']:
            self.getNewSimbol()
            self.comandos()
        else:
            return ''