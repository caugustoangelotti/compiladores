from semantico.simbolo import Simbolo
from semantico.tabelaSimbolos import TabelaSimbolos
from lexico import lexer
from auxiliares import reservedDic as reserved

DEBUG = False
MAKE_TREE = False
PRINT_SYMBOLTABLE = True

class Sintatico:
    def __init__(self, _charsArray):
        self.lexico = lexer.Lexico(_charsArray)
        self.currentSimbol = ""
        self.tabelaSimbolo = TabelaSimbolos()
        self.varType = ""
        self.currentToken = None
        self.insideIf = False
        self.insideElse = False
        self.insideWhile = False
        self.cargaComandosIf = []
        self.cargaComandosElse = []
        self.cargaComandosWhile = []
        self.temp = 0
        self.linhaQuadupla = -1
        self.codigoIntermediario = "<linha;operacao;arg1;arg2;result>\n"
        self.codArr = []

    def populateReservedWords(self):
        for keyWord in reserved.words.values():
            self.tabelaSimbolo.addSymbol(keyWord, Simbolo(keyWord, 'reserved'))

    def geraTemp(self):
        self.temp += 1
        tempVar = 't' + str(self.temp)
        self.tabelaSimbolo.addSymbol(tempVar, Simbolo(tempVar, 'real'))
        return tempVar

    def buildWhileStatement(self, _condicaoDir, arrWhileCommands):
        self.insideWhile = False
        relacaoDir,expressao1Dir,expressao2Dir,condicaoDir = _condicaoDir.split(':')
        self.geraCodigo(relacaoDir,expressao1Dir,expressao2Dir,condicaoDir)
        linhaRelacao = self.linhaQuadupla
        self.geraCodigo('JF', condicaoDir, self.linhaQuadupla + len(arrWhileCommands) + 3, '')
        #'+:{outrosTermosEsq}:{outrosTermos1Dir}:{outrosTermosDir}'
        for command in arrWhileCommands:
            op,exp1,exp2,result = command.split(':')
            if op == 'read':
                self.geraCodigo(op,'','',exp1)
            elif op == 'write':
                self.geraCodigo(op,exp1,'','')
            elif op == '+':
                self.geraCodigo(op,exp1,exp2,result)
            elif op == '-':
                self.geraCodigo(op,exp1,exp2,result)
            elif op == '*':
                self.geraCodigo(op,exp1,exp2,result)
            elif op == '/':
                self.geraCodigo(op,exp1,exp2,result)
            #assigment
            else:
                self.geraCodigo(':=',exp1,'',exp2)

        self.geraCodigo('goto', linhaRelacao, '','')
        self.cargaComandosWhile = []
        
    def buildIfStatement(self, _condicaoDir,arrIfCommands, arrElseCommands,pfalsaDir):
        self.insideIf = False
        self.insideElse = False

        #f'{relacaoDir}:{expressao1Dir}:{expressao2Dir}:{condicaoDir}'
        relacaoDir,expressa1Dir,expressao2Dir,condicaoDir = _condicaoDir.split(':')

        self.geraCodigo(relacaoDir,expressa1Dir,expressao2Dir,condicaoDir)
        self.geraCodigo('JF', condicaoDir, self.linhaQuadupla + len(arrIfCommands) + 3, '')
        for command in arrIfCommands:
            op,exp1,exp2,result = command.split(':')
            if op == 'read':
                self.geraCodigo(op,'','',exp1)
            elif op == 'write':
                self.geraCodigo(op,exp1,'','')
            elif op == '+':
                self.geraCodigo(op,exp1,exp2,result)
            elif op == '-':
                self.geraCodigo(op,exp1,exp2,result)
            elif op == '*':
                self.geraCodigo(op,exp1,exp2,result)
            elif op == '/':
                self.geraCodigo(op,exp1,exp2,result)
            #assigment
            else:
                self.geraCodigo(':=',exp1,exp2,result)
        if not pfalsaDir == '':
            self.geraCodigo('goto', self.linhaQuadupla + len(arrElseCommands) + 2, '', '')
            for command in arrElseCommands:
                op,exp1,exp2,result = command.split(':')
                if op == 'read':
                    self.geraCodigo(op,'','',exp1)
                elif op == 'write':
                    self.geraCodigo(op,exp1,'','')
                elif op == '+':
                    self.geraCodigo(op,exp1,exp2,result)
                elif op == '-':
                    self.geraCodigo(op,exp1,exp2,result)
                elif op == '*':
                    self.geraCodigo(op,exp1,exp2,result)
                elif op == '/':
                    self.geraCodigo(op,exp1,exp2,result)
                #assigment
                else:
                    self.geraCodigo(':=',exp1,exp2,result)
        self.cargaComandosElse = []
        self.cargaComandosIf = []

    def symbolTableContais(self, var):
        return self.tabelaSimbolo.containsKey(var)
    
    def getQuaduplaNewLine(self):
        self.linhaQuadupla += 1
        return self.linhaQuadupla

    def geraCodigo(self, op, arg1, arg2,result):
        codigo = f"{self.getQuaduplaNewLine()};{op};{arg1};{arg2};{result}\n"
        self.codArr.append(codigo.strip())
        self.codigoIntermediario += codigo

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
                print(self.codArr)
        except RuntimeError as err:
            print(err)
            exit()

    def programa(self):
        if MAKE_TREE:
            print('<programa>')

        if self.currentSimbol == reserved.words['program']:
            self.getNewSimbol()
            if self.currentSimbol == reserved.tokenTypes['ident']:
                if self.symbolTableContais(self.currentToken.getTokenValue):
                    raise RuntimeError("Identificar do programa não pode ser uma palavra reservada")
                self.tabelaSimbolo.addSymbol(self.currentToken.getTokenValue(), Simbolo(self.currentToken.getTokenValue(), 'programIdentifier'))
                self.geraCodigo('programname', self.currentToken.getTokenValue(), "", "")
                self.getNewSimbol()
                self.corpo()
                if(self.currentSimbol == reserved.literais['ponto']):
                    return True
                else:
                    raise RuntimeError(f"Erro sintatico esperado . na linha {self.lexico.lineCount}")
            else:
                raise RuntimeError(f"Erro sintatico esperado ident na linha {self.lexico.lineCount}")
        else:
            raise RuntimeError(f"Erro sintatico esperando program na linha {self.lexico.lineCount}")

    def corpo(self):
        if MAKE_TREE:
            print('<corpo>')

        self.dc()
        if(self.currentSimbol == reserved.words['begin']):
            self.getNewSimbol()
            self.comandos()
            if(self.currentSimbol == reserved.words['end']):
                self.getNewSimbol()
                self.geraCodigo('PARA','','','')
            else:
                raise RuntimeError(f"Erro sintatico esperado end na linha {self.lexico.lineCount}")
        else:
            raise RuntimeError(f"Erro sintatico esperado begin na linha {self.lexico.lineCount}")

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
                self.varType = reserved.tokenTypes['real']
            else:
                self.varType = reserved.tokenTypes['real']

            self.getNewSimbol()
        else:
            raise RuntimeError(f"Erro sintatico esperado real ou integer na linha {self.lexico.lineCount}")

    def variaveis(self):
        if MAKE_TREE:
            print('<variaveis>')

        if self.currentSimbol == reserved.tokenTypes['ident']:
            if self.symbolTableContais(self.currentToken.getTokenValue()):
                raise RuntimeError('Erro semantico variavel ja declarada!!!!')
            else:
                self.tabelaSimbolo.addSymbol(self.currentToken.getTokenValue(), Simbolo(self.currentToken.getTokenValue(), self.varType))
                self.geraCodigo('ALME', "0.0", "", self.currentToken.getTokenValue())
            self.getNewSimbol()
            self.mais_var()
        else:
            raise RuntimeError(f'Erro sintatico sintatico esperando ident na linha {self.lexico.lineCount}')

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
            operadorLogico = self.currentToken
            if operadorLogico.getTokenType() == 'MAIOR_IGUAL':
                operadorLogico = ">="
            elif operadorLogico.getTokenType() == 'MENOR_IGUAL':
                operadorLogico = "<="
            elif operadorLogico.getTokenType() == 'DIFERENTE':
                operadorLogico = "<>"
            else:
                operadorLogico = operadorLogico.getTokenType()
            self.getNewSimbol()
            return operadorLogico
        else:
            raise RuntimeError(f"Erro sintatico esperando um operador logico na linha {self.lexico.lineCount}")

    def condicao(self):
        if MAKE_TREE:
            print('<condicao>')

        expressao1Dir = self.expressao()
        relacaoDir = self.relacao()
        expressao2Dir = self.expressao()
        condicaoDir = self.geraTemp()
        #self.geraCodigo(relacaoDir, exp1Dir, exp2Dir, condicaoDir)
        return f'{relacaoDir}:{expressao1Dir}:{expressao2Dir}:{condicaoDir}'

    def comando(self):
        if MAKE_TREE:
            print('<comando>')
        if self.currentSimbol == reserved.words['read'] or self.currentSimbol == reserved.words['write']:
            comando = self.currentToken.getTokenType()
            self.getNewSimbol()
            if self.currentSimbol == reserved.literais['abre_parenteses']:
                self.getNewSimbol()
                if self.currentSimbol == reserved.tokenTypes['ident']:
                    variavel = self.currentToken.getTokenValue()
                    if not self.symbolTableContais(variavel):
                        raise RuntimeError(f"Erro semantico tentando ler ou imprimir variavel não declarada na linha {self.lexico.lineCount}")
                    self.getNewSimbol()
                    if self.insideIf:
                        self.cargaComandosIf.append(f'{comando}:{variavel}:any:any')
                    elif self.insideElse:
                        self.cargaComandosElse.append(f'{comando}:{variavel}:any:any')
                    elif self.insideWhile:
                        self.cargaComandosWhile.append(f'{comando}:{variavel}:any:any')
                    else:
                        if comando == reserved.words['read']:
                            self.geraCodigo('read', '', '', variavel)
                        else:
                            self.geraCodigo('write', variavel, '', '')

                else:
                    raise RuntimeError(f'Erro sintatico esperado identificador na linha {self.lexico.lineCount}')
                if self.currentSimbol == reserved.literais['fecha_parenteses']:
                    self.getNewSimbol()
                else:
                    raise RuntimeError(f'Erro sintatico esperado ) na linha {self.lexico.lineCount}')
            else:
                raise RuntimeError(f"Erro sintatico esperado ( na linha {self.lexico.lineCount}")
        elif self.currentSimbol == reserved.tokenTypes['ident']:
            variavel = self.currentToken
            self.getNewSimbol()
            if self.currentSimbol == reserved.tokenTypes['atribuicao']:
                self.getNewSimbol()
                if self.symbolTableContais(variavel.getTokenValue()):
                    expressaoDir = self.expressao()
                    if self.insideIf:
                        self.cargaComandosIf.append(f'ASSIGMENT:{expressaoDir}:{variavel.getTokenValue()}:any')
                    elif self.insideElse:
                        self.cargaComandosElse.append(f'ASSIGMENT:{expressaoDir}:{variavel.getTokenValue()}:any')
                    elif self.insideWhile:
                        self.cargaComandosWhile.append(f'ASSIGMENT:{expressaoDir}:{variavel.getTokenValue()}:any')
                    else:
                        self.geraCodigo(':=',expressaoDir," ", variavel.getTokenValue())
                else:
                    raise RuntimeError(f'Erro semantico atribuicao de valor a variavel não declarada na linha {self.lexico.lineCount}')
            else:
                raise RuntimeError(f'Erro sintatico esperado := na linha {self.lexico.lineCount}')
        elif self.currentSimbol == reserved.words['if']:
            self.insideIf = True
            self.insideElse = False
            self.insideWhile = False

            self.getNewSimbol()
            condicaoDir = self.condicao()
            if self.currentSimbol == reserved.words['then']:
                self.getNewSimbol()
                self.comandos()
                
                pfalsaDir = self.pfalsa()
                if self.currentSimbol == reserved.literais['dollar']:
                    self.buildIfStatement(condicaoDir, self.cargaComandosIf,self.cargaComandosElse, pfalsaDir)
                    self.getNewSimbol()
                else:
                    raise RuntimeError(f'Erro sintatico esperado $ na linha {self.lexico.lineCount}')
            else:
                raise RuntimeError(f'Erro sintatico esperado then na linha {self.lexico.lineCount}')
        elif self.currentSimbol == reserved.words['while']:
            self.insideIf = False
            self.insideElse = False
            self.insideWhile = True
            self.getNewSimbol()
            condicaoDir = self.condicao()
            if self.currentSimbol == reserved.words['do']:
                self.getNewSimbol()
                self.comandos()
                if self.currentSimbol == reserved.literais['dollar']:
                    self.buildWhileStatement(condicaoDir, self.cargaComandosWhile)
                    self.getNewSimbol()
                else:
                    raise RuntimeError(f'Erro sintatico esperado $ na linha {self.lexico.lineCount}')
        else:
            raise RuntimeError(f'Erro sintatico esperando comando ou identificador na linha {self.lexico.lineCount}')
                
    def expressao(self):
        if MAKE_TREE:
            print('<expressao>')
        termoDir = self.termo()
        outrosTermosDir = self.outros_termos(termoDir)
        return outrosTermosDir

    def termo(self):
        if MAKE_TREE:
            print('<termo>')

        #self.op_un()

        if self.currentSimbol == reserved.tokenTypes['subtracao']:
            self.getNewSimbol()
            fatorDir = self.fator()
            termoDir = self.geraTemp()
            maisFatores1Dir = self.mais_fatores(fatorDir)
            #self.mais_fatores(termoDir)
            self.geraCodigo('uminus', fatorDir, '', termoDir)
            return termoDir
        else:
            fatorDir = self.fator()
            maisFatoresDir = self.mais_fatores(fatorDir)
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
            raise RuntimeError(f'Erro sintatico esperado + ou - na linha {self.lexico.lineCount}')

    def op_mul(self):
        if MAKE_TREE:
            print('<op_mul>')

        if self.currentSimbol == reserved.tokenTypes['multiplicacao'] or self.currentSimbol == reserved.tokenTypes['divisao']:
            self.getNewSimbol()
        else:
            raise RuntimeError(f'Erro sintatico esperado * ou / na linha {self.lexico.lineCount}')

    def outros_termos(self, outrosTermosEsq):
        if MAKE_TREE:
            print('<outros_termos>')

        if self.currentSimbol == reserved.tokenTypes['subtracao'] or self.currentSimbol == reserved.tokenTypes['adicao']:
            sinalMatematico = '+' if self.currentToken.getTokenType() == 'SOMA' else '-'

            #tratamento sintatico
            self.op_add()

            termoDir = self.termo()
            outrosTermosDir = self.geraTemp()
            outrosTermos1Dir = self.outros_termos(termoDir)
            if sinalMatematico == '+':
                if self.insideIf:
                    self.cargaComandosIf.append(f'+:{outrosTermosEsq}:{outrosTermos1Dir}:{outrosTermosDir}')
                elif self.insideElse:
                    self.cargaComandosElse.append(f'+:{outrosTermosEsq}:{outrosTermos1Dir}:{outrosTermosDir}')
                elif self.insideWhile:
                    self.cargaComandosWhile.append(f'+:{outrosTermosEsq}:{outrosTermos1Dir}:{outrosTermosDir}')
                else:
                    self.geraCodigo('+', outrosTermosEsq, outrosTermos1Dir, outrosTermosDir)
            else:
                if self.insideIf:
                    self.cargaComandosIf.append(f'-:{outrosTermosEsq}:{outrosTermos1Dir}:{outrosTermosDir}')
                elif self.insideElse:
                    self.cargaComandosElse.append(f'-:{outrosTermosEsq}:{outrosTermos1Dir}:{outrosTermosDir}')
                elif self.insideWhile:
                    self.cargaComandosWhile.append(f'-:{outrosTermosEsq}:{outrosTermos1Dir}:{outrosTermosDir}')
                else:
                    self.geraCodigo('-', outrosTermosEsq, outrosTermos1Dir, outrosTermosDir)

            return outrosTermosDir
        else:
            return outrosTermosEsq

    def mais_fatores(self, maisFatoresEsq):
        if MAKE_TREE:
            print('<mais_fatores>')

        if self.currentSimbol == reserved.tokenTypes['multiplicacao'] or self.currentSimbol == reserved.tokenTypes['divisao']:
            sinalMatematico = '*' if self.currentToken.getTokenType() == 'MULT' else '/'

            #tratamento sintatico
            self.op_mul()

            fatorDir = self.fator()
            maisFatores1Dir = self.mais_fatores(fatorDir)
            maisFatoresDir = self.geraTemp()
            if sinalMatematico == '*':
                if self.insideIf:
                    self.cargaComandosIf.append(f'*:{maisFatoresEsq}:{maisFatores1Dir}:{maisFatoresDir}')
                elif self.insideElse:
                    self.cargaComandosElse.append(f'*:{maisFatoresEsq}:{maisFatores1Dir}:{maisFatoresDir}')
                elif self.insideWhile:
                    self.cargaComandosWhile.append(f'*:{maisFatoresEsq}:{maisFatores1Dir}:{maisFatoresDir}')
                else:
                    self.geraCodigo('*', maisFatoresEsq, maisFatores1Dir, maisFatoresDir)
            else:
                if self.insideIf:
                    self.cargaComandosIf.append(f'/:{maisFatoresEsq}:{maisFatores1Dir}:{maisFatoresDir}')
                elif self.insideElse:
                    self.cargaComandosElse.append(f'/:{maisFatoresEsq}:{maisFatores1Dir}:{maisFatoresDir}')
                elif self.insideWhile:
                    self.cargaComandosWhile.append(f'/:{maisFatoresEsq}:{maisFatores1Dir}:{maisFatoresDir}')
                else:
                    self.geraCodigo('/', maisFatoresEsq, maisFatores1Dir, maisFatoresDir)
            return maisFatoresDir

        else:
            return maisFatoresEsq

    def fator(self):
        if MAKE_TREE:
            print('<fator>')
        fatorDir = ""
        if self.currentSimbol == reserved.tokenTypes['ident'] or self.currentSimbol == reserved.tokenTypes['numero_int'] or self.currentSimbol == reserved.tokenTypes['numero_real']:
            if self.currentSimbol == reserved.tokenTypes['ident']:
                if not self.symbolTableContais(self.currentToken.getTokenValue()):
                    raise RuntimeError(f'Erro semantico operacao matematica com variavel não declarada na linha {self.lexico.lineCount}')
                fatorDir = self.currentToken.getTokenValue()
            
            else:
                fatorDir = self.currentToken.getTokenValue()

            self.getNewSimbol()
        elif self.currentSimbol == reserved.literais['abre_parenteses']:
            self.getNewSimbol()
            fatorDir = self.expressao()
            if self.currentSimbol == reserved.literais['fecha_parenteses']:
                self.getNewSimbol()
            else:
                raise RuntimeError(f'Erro sintatico esperado ) na linha {self.lexico.lineCount}')
        else:
            raise RuntimeError(f'Erro sintatico esperado variavel, numero: int ou real na linha {self.lexico.lineCount}')
        return fatorDir

    def pfalsa(self):
        if MAKE_TREE:
            print('<pfalsa>')

        if self.currentSimbol == reserved.words['else']:
            self.insideIf = False
            self.insideElse = True
            self.insideWhile = False
            self.getNewSimbol()
            self.comandos()
        else:
            return ''