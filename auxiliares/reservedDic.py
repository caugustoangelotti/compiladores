operadoresLogicos = {
    'igual' : '=',
    'maior' : '>',
    'menor' : '<',
}

literais = {
    'dollar' : '$',
    'ponto_e_virgula' : ';',
    'virgula' : ',',
    'abre_parenteses' : '(',
    'fecha_parenteses' : ')',
    'ponto' : '.',
    'dois_pontos' : ':'
}
tipos = {
    'int' : 'integer', 
    'real' : 'real'
}

matematicos = {
    'mais' : '+', 
    'menos' : '-', 
    'mult' : '*', 
    'div' : '/'
}

words = {
    'program' : 'program',
    'integer' : 'integer',
    'real' : 'real',
    'write' : 'write', 
    'read'  : 'read',
    'if' : 'if',
    'then' : 'then',
    'else' : 'else',
    'begin' : 'begin',
    'end' : 'end',
    'while' : 'while',
    'do' : 'do'

}

tokenTypes = {
    'ident' : 'ident',
    'integer' : 'integer',
    'real' : 'real',
    'numero_int' : 'numero_int',
    'numero_real' : 'numero_real',
    'multiplicacao' : 'MULT',
    'divisao' : 'DIV',
    'adicao' : 'SOMA',
    'subtracao' : 'SUB',
    'maior_igual' : 'MAIOR_IGUAL',
    'menor_igual' : 'MENOR_IGUAL',
    'diferente' : 'DIFERENTE',
    'atribuicao' : 'ATRIBUICAO'
}

mathTokenTypes = {
    'multiplicacao' : 'MULT',
    'divisao' : 'DIV',
    'adicao' : 'SOMA',
    'subtracao' : 'SUB',
}

logicTokenTypes = {
    'maior_igual' : 'MAIOR_IGUAL',
    'menor_igual' : 'MENOR_IGUAL',
    'diferente' : 'DIFERENTE',
    'igual' : '=',
    'maior' : '>',
    'menor' : '<'
}