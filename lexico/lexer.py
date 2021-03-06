from lexico.token import Token
import auxiliares.charConstants as charsdic

class Lexico:
    def __init__(self, _charArr):
        self.cursorPos = -1
        self.charArr = _charArr
        self.estado = 0
        self.lineCount = 1
        self.reservedWords = ['program', 'begin', 'end', 'if', 'then', 'else', 'read', 'write', 'real', 'integer', 'while', 'do']
    
    def getLine(self):
        return self.lineCount
    def is_letra(self, _char):
        return _char in charsdic.ALFABETO

    def is_espaco(self, _char):
        return _char in charsdic.ESPACOS

    def is_numero(self, _char):
        return _char in charsdic.NUMEROS

    def is_literal(self, _char):
        return _char in charsdic.LITERAIS

    def nextChar(self):
        if self.cursorPos == len(self.charArr) - 1:
            return None
        self.cursorPos += 1
        return self.charArr[self.cursorPos]
    
    def isEOF(self):
        return self.cursorPos == len(self.charArr)
    
    def cursorStepForward(self):
        self.cursorPos += 1

    def cursorStepBack(self):
        self.cursorPos -= 1
    
    def getCursorPos(self):
        return self.cursorPos

    def getCurrentChar(self):
        if self.isEOF():
            return None
        return self.charArr[self.cursorPos]
    
    def nexToken(self):
        ident = ""
        numero = ""
        fator = ""
        while(True):
            try:
                if self.estado == 0:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if self.is_letra(char):
                        ident += char
                        self.estado = 1
                    elif self.is_numero(char):
                        numero += char
                        self.estado = 3
                    elif self.is_literal(char):
                        self.estado = 7
                    elif self.is_espaco(char):
                        if char == '\n':
                            self.lineCount += 1
                        self.estado = 23
                    else:
                        raise Exception("Caractere n??o reconhecido encontrado, encerrando...")
                elif self.estado == 1:
                    delimiter = self.nextChar()
                    if delimiter == None:
                        return None
                    if not (self.is_espaco(delimiter) or self.is_literal(delimiter)):
                        ident += self.getCurrentChar()
                    else:
                        self.estado = 2
                elif self.estado == 2:
                        if ident in self.reservedWords:
                            tkn = Token(ident,ident)
                            self.cursorStepBack()
                        else:
                            tkn = Token('ident', ident)
                            self.cursorStepBack()
                        ident = ""
                        #self.cursorStepBack()
                        self.estado = 0
                        return tkn
                elif self.estado == 3:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if not (self.is_espaco(char) or self.is_literal(char)):
                        numero += char
                        self.estado = 3
                    else:
                        if char == '.':
                            if(self.nextChar() == '.'):
                                raise Exception(f'Erro na declaracao de valor real na linha {self.getLine()}')
                            else:
                                self.estado = 4
                            self.cursorStepBack()
                        else:
                            self.estado = 6
                elif self.estado == 4:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if not (self.is_espaco(char) or self.is_literal(char)):
                        fator += char
                    else:
                        self.estado = 5
                elif self.estado == 5:
                    tkn = Token('numero_real', f"{numero}.{fator}")
                    numero = ""
                    fator = ""
                    self.cursorStepBack()
                    self.estado = 0
                    return tkn
                elif self.estado == 6:
                    tkn = Token('numero_int', numero)
                    numero = ""
                    self.cursorStepBack()
                    self.estado = 0
                    return tkn
                elif self.estado == 7:
                    char = self.getCurrentChar()
                    if char == None:
                        return None
                    if char == '>':
                        self.estado = 8
                    elif char == '<':
                        self.estado = 11
                    elif char == ':':
                        self.estado = 15
                    elif char == '+':
                        self.estado = 18
                    elif char == '-':
                        self.estado = 19
                    elif char == '*':
                        self.estado = 20
                    elif char == '/':
                        self.estado = 21
                    elif char == '{':
                        self.estado = 24
                    else:
                        self.estado = 22
                elif self.estado == 8:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if char == '=':
                        self.estado = 9
                    else:
                        self.estado = 10
                elif self.estado == 9:
                    tkn = Token("MAIOR_IGUAL")
                    self.estado = 0
                    #self.cursorStepForward()
                    return tkn
                elif self.estado == 10:
                    self.cursorStepBack()
                    tkn = Token(self.getCurrentChar())
                    self.estado = 0
                    #self.cursorStepForward()
                    return tkn
                elif self.estado == 11:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if char == ">":
                        self.estado = 12
                    elif char == "=":
                        self.estado = 13
                    else:
                        self.estado = 14
                elif self.estado == 12:
                    tkn = Token('DIFERENTE')
                    self.estado = 0
                    #self.cursorStepForward()
                    return tkn
                elif self.estado == 13:
                    tkn = Token('MENOR_IGUAL')
                    self.estado = 0
                    #self.cursorStepForward()
                    return tkn
                elif self.estado == 14:
                    self.cursorStepBack()
                    tkn = Token(self.getCurrentChar())
                    self.estado = 0
                    #self.cursorStepForward()
                    return tkn

                elif self.estado == 15:
                    char = self.nextChar()
                    if char == '=':
                        self.estado = 16
                    else:
                        self.estado = 17
                elif self.estado == 16:
                    tkn = Token("ATRIBUICAO")
                    self.estado = 0
                    #elf.cursorStepForward()
                    return tkn
                elif self.estado == 17:
                    self.cursorStepBack()
                    tkn = Token(self.getCurrentChar())
                    self.estado = 0
                    #self.cursorStepForward()
                    return tkn
                elif self.estado == 18:
                    tkn = Token('SOMA', self.getCurrentChar())
                    self.estado = 0
                    return tkn
                elif self.estado == 19:
                    tkn = Token('SUB', self.getCurrentChar())
                    self.estado = 0
                    return tkn
                elif self.estado == 20:
                    tkn = Token('MULT', self.getCurrentChar())
                    self.estado = 0
                    return tkn
                elif self.estado == 21:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if char == '*':
                        self.estado = 25
                    else:
                        tkn = Token('DIV', self.getCurrentChar())
                        self.cursorStepBack()
                        self.estado = 0
                        return tkn
                elif self.estado == 22:
                    tkn = Token(self.getCurrentChar())
                    self.estado = 0
                    return tkn
                elif self.estado == 23:
                    self.estado = 0
                elif self.estado == 24:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if char == '}':
                        self.estado = 0
                    else:
                        self.estado = 24
                elif self.estado == 25:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if char == '*':
                        self.estado = 26
                    else:
                        self.estado = 25
                elif self.estado == 26:
                    char = self.nextChar()
                    if char == None:
                        return None
                    if char == '/':
                        self.estado = 0
                    elif char == '*':
                        self.estado = 26
                    else:
                        self.estado = 25
                else:
                    raise Exception("Estado n??o definido no analisador lexico encerrando...")
            except Exception as err:
                print(err)
                exit()