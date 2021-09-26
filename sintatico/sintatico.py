from semantico.simbolo import Simbolo
from semantico.tabelaSimbolos import TabelaSimbolos
from lexico import lexer
from auxiliares import reservedDic as reserved

DEBUG = True
MAKE_TREE = False
PRINT_SYMBOLTABLE = False

class Sintatico:
    def __init__(self, _charsArray):
        self.lexico = lexer.Lexico(_charsArray)
        self.currentSimbol = ""
        self.tabelaSimbolo = TabelaSimbolos()
        self.varType = ""
        self.currentToken = None
        self.temp = 0
        self.linhaQuadupla = -1
        self.codigoIntermediario = "<linha;operacao;arg1;arg2;result>\n"


    def populateReservedWords(self):
        for keyWord in reserved.words.values():
            self.tabelaSimbolo.addSymbol(keyWord, Simbolo(keyWord, 'reserved'))

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
            self.populateReservedWords()
            self.getNewSimbol()
            if self.programa():
                print('\nAnalise sintatica e semantica completada\n')
                if PRINT_SYMBOLTABLE:
                    print('##########SYMBOL-TABLE############\n')
                    for key in self.tabelaSimbolo.symbolTable.keys():
                        print(self.tabelaSimbolo.getSymbol(key))
                    print('\n##################################\n')

                print('#######CODIGO_INTERMEDIARIO#######\n')
                print(self.codigoIntermediario)
                print('##################################\n')
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
            self.getNewSimbol()
            if self.currentSimbol == reserved.literais['abre_parenteses']:
                self.getNewSimbol()
                if self.currentSimbol == reserved.tokenTypes['ident']:
                    self.getNewSimbol()
                else:
                    raise RuntimeError('Erro sintatico esperado identificador')
                if self.currentSimbol == reserved.literais['fecha_parenteses']:
                    self.getNewSimbol()
                else:
                    raise RuntimeError('Erro sintatico esperado )')
            else:
                raise RuntimeError("Erro sintatico esperado (")
        elif self.currentSimbol == reserved.tokenTypes['ident']:
            self.getNewSimbol()
            if self.currentSimbol == reserved.tokenTypes['atribuicao']:
                self.getNewSimbol()
                self.expressao()
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
        self.termo()
        self.outros_termos()

    def termo(self):
        if MAKE_TREE:
            print('<termo>')

        self.op_un()
        self.fator()
        self.mais_fatores()

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

    def outros_termos(self):
        if MAKE_TREE:
            print('<outros_termos>')

        if self.currentSimbol == reserved.tokenTypes['subtracao'] or self.currentSimbol == reserved.tokenTypes['adicao']:
            self.op_add()
            self.termo()
            self.outros_termos()
        else:
            return ''

    def mais_fatores(self):
        if MAKE_TREE:
            print('<mais_fatores>')

        if self.currentSimbol == reserved.tokenTypes['multiplicacao'] or self.currentSimbol == reserved.tokenTypes['divisao']:
            self.op_mul()
            self.fator()
            self.mais_fatores()
        else:
            return ''

    def fator(self):
        if MAKE_TREE:
            print('<fator>')

        if self.currentSimbol == reserved.tokenTypes['ident'] or self.currentSimbol == reserved.tokenTypes['numero_int'] or self.currentSimbol == reserved.tokenTypes['numero_real']:
            self.getNewSimbol()

        elif self.currentSimbol == reserved.literais['abre_parenteses']:
            self.getNewSimbol()
            self.expressao()
            if self.currentSimbol == reserved.literais['fecha_parenteses']:
                self.getNewSimbol()
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