import os
from lexico.lexer import Lexico

os.system('cls')

with open("codigo.txt", "r", encoding='utf-8') as file:
    fileToStringArr = file.read()

lex = Lexico(fileToStringArr)

tknResponse = lex.nexToken()
while tknResponse != None:
    if(tknResponse != None):
        print(tknResponse)
    tknResponse = lex.nexToken()