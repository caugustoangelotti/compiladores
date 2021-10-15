import string

class CodigoHipotetico:
    def __init__(self, _tabelaSimbolos, _codigoObjeto, _arrTemporarios) -> None:
        self.tabelaSimbolos = _tabelaSimbolos
        self.codigoObjeto = _codigoObjeto
        self.arrTemporarios = _arrTemporarios
        self.codHipoteticoArr = []
        self.dataArr = []
        self.logicLine = 0
        self.objectCodeToHipoteticCode()
        self.geraArquivoCodHipotetico()

    def geraArquivoCodHipotetico(self):
        with open('output.maqhipo.txt', 'w') as file:
            for line in self.codHipoteticoArr:
                file.write(f'{line.strip()}\n')
        return True
    def is_digit(self, str):
        return str in string.digits

    def countCommands(self,_op,_target,arr):
        #uminus,read,write,assigment = 2
        #matematicas e logicas 3
        commandsLen = 0
        if _op == 'JF':
            for code in arr:
                linha,op,arg1,arg2,result = code.split(';')
                if op == 'uminus' or op == 'read' or op == 'write' or op == ':=':
                    commandsLen += 2
                elif op == 'goto':
                    commandsLen += 1
                else:
                    commandsLen += 3
                if linha == _target:
                    return commandsLen
        else:
            for code in arr:
                linha,op,arg1,arg2,result = code.split(';')
                if op == 'uminus' or op == 'read' or op == 'write' or op == ':=':
                    commandsLen += 2
                elif op == 'JF':
                    commandsLen += 1
                else:
                    commandsLen += 3
                if linha == _target:
                    return commandsLen

    def getVarRelativePos(self,var):
        return self.tabelaSimbolos.getSymbol(var).getEnderecoRelativo()
    
    def argIsTempVar(self, var):
        return var in self.arrTemporarios

    def objectCodeToHipoteticCode(self):
        self.codHipoteticoArr.append('INPP')
        """ for temp in self.arrTemporarios:
            self.codHipoteticoArr.append('ALME 0.0')
            self.dataArr.append(0.0) """
        for i,instrucao in enumerate(self.codigoObjeto):
            linha,ins,arg1,arg2,result = instrucao.split(';')
            if ins == 'ALME':
                self.codHipoteticoArr.append('ALME 0.0')
                self.dataArr.append(0.0)
            elif ins == 'read':
                self.codHipoteticoArr.append('LEIT')
                self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
            elif ins == 'write':
                self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                self.codHipoteticoArr.append(f'IMPR')
            elif ins == 'uminus':
                if self.is_digit(arg1):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'INVE')
                else:
                    pass
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'INVE')
            elif ins == '+':
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'SOMA')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')

                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'SOMA')
                        self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'SOMA')
                        self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'SOMA')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')

            elif ins == '-':
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'SUBT')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')

                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'SUBT')
                        self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'SUBT')
                        self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'SUBT')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
            elif ins == '*':
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'MULT')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')

                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'MULT')
                        self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'MULT')
                        self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'MULT')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
            elif ins == '/':
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'DIV')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')

                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'DIV')
                        self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'DIV')
                        self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'DIV')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
            elif ins == ':=':
                if self.is_digit(arg1):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'ARMZ {self.getVarRelativePos(result)}')
            elif ins == '>':
                self.logicLine = len(self.codHipoteticoArr)
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'CPMA')
                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'CPMA')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'CPMA')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'CPMA')
            elif ins == '<':
                self.logicLine = len(self.codHipoteticoArr)
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'CPME')
                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'CPME')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'CPME')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'CPME')
            elif ins == '<>':
                self.logicLine = len(self.codHipoteticoArr)
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'CDES')
                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'CDES')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'CDES')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'CDES')
            elif ins == '=':
                self.logicLine = len(self.codHipoteticoArr)
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'CPIG')
                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'CPIG')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'CPIG')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'CPIG')
            elif ins == '>=':
                self.logicLine = len(self.codHipoteticoArr)
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'CMAI')
                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'CMAI')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'CMAI')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'CMAI')
            elif ins == '<=':
                self.logicLine = len(self.codHipoteticoArr)
                if self.is_digit(arg1) and self.is_digit(arg2):
                    self.codHipoteticoArr.append(f'CRCT {arg1}')
                    self.codHipoteticoArr.append(f'CRCT {arg2}')
                    self.codHipoteticoArr.append(f'CPMI')
                elif self.is_digit(arg1) or self.is_digit(arg2):
                    if self.is_digit(arg1):
                        self.codHipoteticoArr.append(f'CRCT {arg1}')
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                        self.codHipoteticoArr.append(f'CPMI')
                    else:
                        self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                        self.codHipoteticoArr.append(f'CRCT {arg2}')
                        self.codHipoteticoArr.append(f'CPMI')
                else:
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg1)}')
                    self.codHipoteticoArr.append(f'CRVL {self.getVarRelativePos(arg2)}')
                    self.codHipoteticoArr.append(f'CPMI')
            elif ins == 'JF':
                self.codHipoteticoArr.append(f'DSVF {(len(self.codHipoteticoArr) + self.countCommands(ins,arg2,self.codigoObjeto[i + 1:])) - 1}')
            elif ins == 'goto':
                if linha > arg1:
                    self.codHipoteticoArr.append(f'DSVI {self.logicLine}')
                else:
                    self.codHipoteticoArr.append(f'DSVI {(len(self.codHipoteticoArr) + self.countCommands(ins,arg1,self.codigoObjeto[i + 1:])) - 2}')

        self.codHipoteticoArr.append('PARA')