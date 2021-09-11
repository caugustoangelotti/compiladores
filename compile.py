from lexico.lexer import Lexico as lx

with open("codigo.txt", "r", encoding='utf-8') as file:
    fileToStringArr = file.read()

lex = lx.Lexico(fileToStringArr)

tknResponse = lex.nexToken()
while tknResponse != None:
    if(tknResponse != None):
        print(tknResponse)
    tknResponse = lex.nexToken()