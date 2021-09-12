import os
import sys
from lexico.lexer import Lexico

#os.system('cls')
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


""" tknResponse = lex.nexToken()
while tknResponse != None:
    if(tknResponse != None):
        print(tknResponse)
    tknResponse = lex.nexToken() """