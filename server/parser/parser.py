from ply.lex import lex

reserved = {
    'number': 'NUMBER',
    'float' : 'FLOAT',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'var': 'VAR',
    'const': 'CONST',
    'if': 'IF',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'push': 'PUSH',
    'pop': 'POP',
    'indexOf': 'INDEXOF',
    'join': 'JOIN',
    'length': 'LENGTH',
    'interface': 'INTERFACE',
    'Object': 'OBJECT',
    'keys': 'KEYS',
    'values': 'VALUES',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'console': 'CONSOLE',
    'log': 'LOG',
    'parseInt': 'PARSEINT',
    'parseFloat': 'PARSEFLOAT',
    'toString': 'TOSTRING',
    'toLowerCase': 'TOLOWERCASE',
    'toUpperCase': 'TOOPPERCASE',
    'typeof': 'TYPEOF'
}

tokens = [
    'INCREMENTO',
    'DECREMENTO',
    'MASIGUAL',
    'MENOSIGUAL',
    'MENIGQUE',
    'MAYIGQUE',
    'DOBLEIG',
    'NOIG',
    'OR',
    'AND',
    'DOSPTS',
    'PUNTO',
    'PTCOMA',
    'COMA',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'INTDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'MENQUE',
    'MAYQUE',
    'NOT',
    'IGUAL',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reserved.values())

t_INCREMENTO = r'\+\+' 
t_DECREMENTO = r'--'
t_MASIGUAL   = r'\+='
t_MENOSIGUAL = r'-='
t_MENIGQUE   = r'<='
t_MAYIGQUE   = r'>='
t_DOBLEIG    = r'=='
t_NOIG       = r'!='
t_OR         = r'\|\|'
t_AND        = r'&&'
t_DOSPTS     = r':'
t_PUNTO      = r'\.'
t_PTCOMA     = r';'
t_COMA       = r','
t_LLAVIZQ    = r'{'
t_LLAVDER    = r'}'
t_PARIZQ     = r'\('
t_PARDER     = r'\)'
t_CORIZQ     = r'\['
t_CORDER     = r'\]'
t_INTDER     = r'\?'
t_MAS        = r'\+'
t_MENOS      = r'-'
t_POR        = r'\*'
t_DIVIDIDO   = r'/'
t_MODULO     = r'%' 
t_MENQUE     = r'<' 
t_MAYQUE     = r'>' 
t_NOT        = r'!' 
t_IGUAL      = r'=' 


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print('Error al convertir a entero %d', t.value)
        t.value = 0
    return t


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print('Error al convertir a decimal %d', t.value)
        t.value = 0
    return t


def t_CADENA(t):
    r'\"([^\n\"\\]|\\(n|r|t|\\|\'|\"))*\"'
    t.value = t.value[1:-1]
    return t 


def t_CARACTER(t):
    r'\'([^\n\'\\]|\\(n|r|t|\\|\'|\"))\''
    t.value = t.value[1:-1]
    return t 


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1


def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


t_ignore = ' \t'


def t_error(t):
    print("Error Léxico '%s'" % t.value[0])
    t.lexer.skip(1)

