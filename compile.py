from sintatico.sintatico import Sintatico
from lexico.lexer import Lexico
import sys

DEV = False

#os.system('cls')

if(DEV):
    fileDir = "D:\\DEV\\compiladores\\codigo.txt"
else:
    try:
        fileDir = sys.argv[1]
    except IndexError:
        print("Forneca o nome do arquivo ou caminho do codigo fonte ex:py compile.py C:\\Users\\...")
        exit()

with open(fileDir, 'r', encoding='utf-8') as file:
    fileToCharArr = file.read()


sint = Sintatico(fileToCharArr)
sint.doSyntaxAnalise()


"""
lex = Lexico(fileToCharArr)

 with open("tokens.log.txt", 'a', encoding='utf-8') as arqvLog:
    tknResponse = lex.nexToken()
    arqvLog.writelines("###############################\n")
    while tknResponse != None:
        if(tknResponse != None):
            print(tknResponse)
            arqvLog.writelines(f"{tknResponse.__repr__()}\n")
        tknResponse = lex.nexToken()
    arqvLog.writelines("-------------------------------\n") """