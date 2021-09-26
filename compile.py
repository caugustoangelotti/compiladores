from sintatico.sintatico import Sintatico
from lexico.lexer import Lexico
import sys

DEV = True

#os.system('cls')

if(DEV):
    fileDir = "D:\\DEV\\compiladores\\codigo.txt"
else:
    try:
        fileDir = sys.argv[1]
    except IndexError:
        print("Forneca o caminho do codigo fonte ex:py compile.py C:\\Users\\...")
        exit()

try:
    assert (fileDir != " " and fileDir != ""), "O caminho do arquivo não pode ser vazio"
except Exception as err:
    print(err)
    exit()

#ISSUE: falso positivo em arquivos do mesmo diretorio ao não usar drag and drop
try:
    if "/" in fileDir:
        fileExtension = fileDir.split("/")
        fileExtension = fileExtension[len(fileExtension) - 1]
    elif "\\" in fileDir:
        fileExtension = fileDir.split("\\")
        fileExtension = fileExtension[len(fileExtension) - 1]
    else:
        raise ValueError("O arquivo não tem um diretorio valido")
except ValueError as err:
    print(err)
    exit()

try:
    fileExtension = fileExtension.split('.')
    assert ((fileExtension[1] == 'txt') or fileExtension[1] == 'lalg'), "O arquivo deve ter extensão .txt ou .lalg"
except Exception as err:
    print(err)
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