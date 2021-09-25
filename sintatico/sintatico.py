from semantico.simbolo import Simbolo
from semantico.tabelaSimbolos import TabelaSimbolos
from lexico import lexer
from auxiliares import reservedDic as reserved

DEBUG = False
MAKE_TREE = False

class Sintatico:
    def __init__(self, _charsArray):
        self.lexico = lexer.Lexico(_charsArray)
        self.currentSimbol = ""
        self.tabelaSimbolo = TabelaSimbolos()
        self.varType = ""
        self.currentToken  = None
        self.temp = 0
        self.linhaQuadupla = -1
        self.codigoIntermediario = "<linha;operacao;arg1;arg2;result>\n"
    
    def geraTemp(self):
        self.temp += 1
        return 't' + str(self.temp)
    
    def getQuaduplaNewLine(self):
        self.linhaQuadupla += 1
        return self.linhaQuadupla

    def geraCodigo(self, op, arg1, arg2,result):
        self.codigoIntermediario += f"<{self.getQuaduplaNewLine()};{op};{arg1};{arg2};{result}>\n"

    def getNewSimbol(self):
        tkn = self.lexico.nexToken()
        self.currentToken = tkn
        self.currentSimbol = tkn.getTokenType()
        if(DEBUG):
            tknValue = tkn.getTokenValue()
            print(f'type: {self.currentSimbol}  valor: {tknValue if tknValue != None else ""}')
        return self.currentSimbol

    def doSyntaxAnalise(self):
        try:
            self.getNewSimbol()
            if self.programa():
                print('Analise sintatica e semantica completada')
                print('###GERANDO_CODIGO_INTERMEDIARIO')
                print(self.codigoIntermediario)
        except RuntimeError as err:
            print(err)
            exit()


    def programa(self):
        if MAKE_TREE:
            print('<programa>')

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
        if MAKE_TREE:
            print('<corpo>')

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
        if MAKE_TREE:
            print('<dc>')

        if self.currentSimbol in reserved.tipos.values():
            self.dc_v()
            self.mais_dc()
        else:
            return ''

    def mais_dc(self):
        if MAKE_TREE:
            print('<mais_dc>')

        if self.currentSimbol == reserved.literais['ponto_e_virgula']:
            self.getNewSimbol()
            self.dc()
        else:
            return ''

    def comandos(self):
        if MAKE_TREE:
            print('<comandos>')

        self.comando()
        self.mais_comandos()

    def mais_comandos(self):
        if MAKE_TREE:
            print('<mais_comandos>')

        if self.currentSimbol == reserved.literais['ponto_e_virgula']:
            self.getNewSimbol()
            self.comandos()
        else:
            return ''

    def dc_v(self):
        if MAKE_TREE:
            print('<dc_v>')

        self.tipo_var()
        if self.currentSimbol == reserved.literais['dois_pontos']:
            self.getNewSimbol()
            self.variaveis()
        else:
            raise RuntimeError("Erro sintatico esperando :")
    def tipo_var(self):
        if MAKE_TREE:
            print('<tipo_var>')

        if self.currentSimbol in reserved.tipos.values():
            if self.currentSimbol == 'integer':
                self.varType = reserved.tokenTypes['integer']
            else:
                self.varType = reserved.tokenTypes['real']

            self.getNewSimbol()
        else:
            raise RuntimeError("Erro sintatico esperado real ou integer")
    def variaveis(self):
        if MAKE_TREE:
            print('<variaveis>')

        if self.currentSimbol == reserved.tokenTypes['ident']:
            if self.tabelaSimbolo.containsKey(self.currentToken.getTokenValue()):
                raise RuntimeError('Erro semantico varivael ja declarada!!!!')
            else:
                self.tabelaSimbolo.addSymbol(self.currentToken.getTokenValue(), Simbolo(self.currentToken.getTokenValue(), self.varType))
                if self.varType == 'integer':
                    self.geraCodigo('ALME', "0", "", self.currentToken.getTokenValue())
                else:
                    self.geraCodigo('ALME', "0.0", "", self.currentToken.getTokenValue())


            self.getNewSimbol()
            self.mais_var()
        else:
            raise RuntimeError('Erro sintatico sintatico esperando ident')
    def mais_var(self):
        if MAKE_TREE:
            print('<mais_var>')

        if self.currentSimbol == reserved.literais['virgula']:
            self.getNewSimbol()
            self.variaveis()
        else:
            return ''   
    def relacao(self):
        if MAKE_TREE:
            print('<relacao>')

        if self.currentSimbol in reserved.logicTokenTypes.values():
            self.getNewSimbol()
        else:
            raise RuntimeError("Erro sintatico esperando um operador logico")
    def condicao(self):
        if MAKE_TREE:
            print('<condicao>')

        self.expressao()
        self.relacao()
        self.expressao()
    def comando(self):
        if MAKE_TREE:
            print('<comando>')
        if self.currentSimbol == reserved.words['read'] or self.currentSimbol == reserved.words['write']:
            commandTkn = self.currentToken
            self.getNewSimbol()
            if self.currentSimbol == reserved.literais['abre_parenteses']:
                self.getNewSimbol()
                if self.currentSimbol == reserved.tokenTypes['ident']:
                    if self.tabelaSimbolo.containsKey(self.currentToken.getTokenValue()):
                        if commandTkn.getTokenType() == 'read':
                            self.geraCodigo('read', "", "", self.currentToken.getTokenValue())
                        else:
                            self.geraCodigo('write', self.currentToken.getTokenValue(), "", "")
                        self.getNewSimbol()
                    else:
                        raise RuntimeError(f"Erro semantico tentando atribuir ou ler variavel não declarada")
                    #self.variaveis()
                else:
                    raise RuntimeError('Erro sintatico esperado identificador')
                if self.currentSimbol == reserved.literais['fecha_parenteses']:
                    self.getNewSimbol()
                else:
                    raise RuntimeError('Erro sintatico esperado )')
            else:
                raise RuntimeError("Erro sintatico esperado (")
        elif self.currentSimbol == reserved.tokenTypes['ident']:
            identTkn = self.currentToken
            self.getNewSimbol()
            if self.currentSimbol == reserved.tokenTypes['atribuicao']:
                self.getNewSimbol()
                expressaoDir = self.expressao()
                self.geraCodigo(':=', expressaoDir, "", identTkn.getTokenValue())
            else:
                raise RuntimeError('Erro sintatico esperado :=')
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
                    raise RuntimeError('Erro sintatico esperado $')
            else:
                raise RuntimeError('Erro sintatico esperado then')
        else:
            raise RuntimeError('Erro sintatico esperando comando ou identificador')
                
    def expressao(self):
        if MAKE_TREE:
            print('<expressao>')
        termoDir = self.termo()
        outrosTermosDir = self.outros_termos(termoDir)
        return outrosTermosDir

    def termo(self):
        if MAKE_TREE:
            print('<termo>')

        if self.currentSimbol == reserved.tokenTypes['subtracao']:
            pass
        else:
            pass
        #self.op_un()
        termoDir = self.fator()
        maisFatoresDir = self.mais_fatores(termoDir)
        return maisFatoresDir
    def op_un(self):
        if MAKE_TREE:
            print('<op_un>')

        if self.currentSimbol == reserved.tokenTypes['subtracao']:
            self.getNewSimbol()
        else:
            return ''
    def op_add(self):
        if MAKE_TREE:
            print('<op_add>')

        if self.currentSimbol == reserved.tokenTypes['subtracao'] or self.currentSimbol == reserved.tokenTypes['adicao']:
            self.getNewSimbol()
        else:
            raise RuntimeError('Erro sintatico esperado + ou -')
    def op_mul(self):
        if MAKE_TREE:
            print('<op_mul>')

        if self.currentSimbol == reserved.tokenTypes['multiplicacao'] or self.currentSimbol == reserved.tokenTypes['divisao']:
            self.getNewSimbol()
        else:
            raise RuntimeError('Erro sintatico esperado * ou /')

    def outros_termos(self, outros_termosEsq):
        if MAKE_TREE:
            print('<outros_termos>')

        if self.currentSimbol == reserved.tokenTypes['subtracao'] or self.currentSimbol == reserved.tokenTypes['adicao']:
            #self.op_add()
            operando = self.currentToken.getTokenType()
            self.getNewSimbol()
            termoDir = self.termo()
            outros_termos1Dir = self.outros_termos(termoDir)
            outros_termosDir = self.geraTemp()
            if operando == 'SOMA':
                self.geraCodigo('+', outros_termosEsq, outros_termos1Dir, outros_termosDir)
                return outros_termosDir
            else:
                return outros_termosDir
        else:
            return outros_termosEsq

    def mais_fatores(self,mais_fatoresEsq):
        if MAKE_TREE:
            print('<mais_fatores>')

        if self.currentSimbol == reserved.tokenTypes['multiplicacao'] or self.currentSimbol == reserved.tokenTypes['divisao']:
            #self.op_mul()
            operando = self.currentToken.getTokenType()
            self.getNewSimbol()
            fatorDir = self.fator()
            mais_fatores1Dir = self.mais_fatores(fatorDir)
            mais_fatoresDir = self.geraTemp()
            if operando == 'MULT':
                self.geraCodigo('*', mais_fatoresEsq, mais_fatores1Dir, mais_fatoresDir)
                return mais_fatoresDir
            else:
                self.geraCodigo('/', mais_fatoresEsq, mais_fatores1Dir, mais_fatoresDir)
                return mais_fatoresDir
        else:
            return mais_fatoresEsq

    def fator(self):
        if MAKE_TREE:
            print('<fator>')

        if self.currentSimbol == reserved.tokenTypes['ident'] or self.currentSimbol == reserved.tokenTypes['numero_int'] or self.currentSimbol == reserved.tokenTypes['numero_real']:
            if self.currentSimbol == reserved.tokenTypes['ident']:
                if not self.tabelaSimbolo.containsKey(self.currentToken.getTokenValue()):
                    raise RuntimeError("Erro semantico operacoes com variaveis não declaradas")
                ident = self.currentToken.getTokenValue()
                self.getNewSimbol()
                return ident
            else:
                number = self.currentToken.getTokenValue()
                self.getNewSimbol()
                return number

        elif self.currentSimbol == reserved.literais['abre_parenteses']:
            self.getNewSimbol()
            expressaoDir = self.expressao()
            if self.currentSimbol == reserved.literais['fecha_parenteses']:
                self.getNewSimbol()
                return expressaoDir
            else:
                raise RuntimeError('Erro sintatico esperado )')
        else:
            raise RuntimeError('Erro sintatico esperado variavel, numero: int ou real')

    def pfalsa(self):
        if MAKE_TREE:
            print('<pfalsa>')

        if self.currentSimbol == reserved.words['else']:
            self.getNewSimbol()
            self.comandos()
        else:
            return ''