import parser.ply.lex as lex
import parser.ply.yacc as yacc

from environment.types import ExpressionType
from expressions.primitive import Primitive
from expressions.operation import Operation
from expressions.access import Access
from expressions.array import Array
from expressions.array_access import ArrayAccess
from expressions.pop import Pop
from expressions.index_of import IndexOf
from expressions.join import Join
from expressions.length import Length
from expressions.parse_int import ParseInt
from expressions.parse_float import ParseFloat
from expressions.to_string import ToString
from expressions.lower_case import LowerCase
from expressions.upper_case import UpperCase
from expressions.typeof import Typeof
from expressions.ternary import Ternary

from instructions.console_log import ConsoleLog
from instructions.declaration import Declaration
from instructions.assignment import Assignment
from instructions.array_declaration import ArrayDeclaration
from instructions.push import Push
from instructions.if_instruction import If
from instructions.else_if_instruction import ElseIf
from instructions.else_instruction import Else
from instructions.while_instruction import While

class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column

ast = None

reserved = {
    'number': 'NUMBER',
    'float' : 'FLOAT',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'var': 'VAR',
    'const': 'CONST',
    'if': 'IF',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'of': 'OF',
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
    'toUpperCase': 'TOUPPERCASE',
    'typeof': 'TYPEOF'
}

tokens = [
    'INCREMENTO',
    'DECREMENTO',
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
    'DECIMAL',
    'ENTERO',
    'TRUE',
    'FALSE',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reserved.values())

t_INCREMENTO = r'\+=' 
t_DECREMENTO = r'-='
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


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        float_value = float(t.value)
        params = get_params(t)
        t.value = Primitive(params.line, params.column, float_value, ExpressionType.FLOAT)
    except ValueError:
        print('Error al convertir a decimal %d', t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        int_value = int(t.value)
        params = get_params(t)
        t.value = Primitive(params.line, params.column, int_value, ExpressionType.NUMBER)
    except ValueError:
        print('Error al convertir a entero %d', t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_TRUE(t):
    r'true'
    params = get_params(t)
    t.value = Primitive(params.line, params.column, True, ExpressionType.BOOLEAN)
    return t


def t_FALSE(t):
    r'false'
    params = get_params(t)
    t.value = Primitive(params.line, params.column, False, ExpressionType.BOOLEAN)
    return t


def t_CADENA(t):
    r'\"([^\n\"\\]|\\(n|r|t|\\|\'|\"))*\"'
    str_value = t.value[1:-1]
    params = get_params(t)
    t.value = Primitive(params.line, params.column, str_value, ExpressionType.STRING)
    return t


def t_CARACTER(t):
    r'\'([^\n\'\\]|\\(n|r|t|\\|\'|\"))?\''
    char_value = t.value[1:-1]
    params = get_params(t)
    t.value = Primitive(params.line, params.column, char_value, ExpressionType.CHAR)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMENTARIO_SIMPLE(t):
    r'//.*'
    t.lexer.lineno += 1


def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


t_ignore = ' \t\r'


def t_error(t):
    params = get_params(t)
    ast.set_errors(f'El carácter "{t.value[0]}" no pertenece al lenguaje.', params.line, params.column, 'Léxico')
    t.lexer.skip(1)


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT', 'TYPEOF'),
    ('left', 'MAYQUE', 'MENQUE', 'MAYIGQUE', 'MENIGQUE', 'DOBLEIG', 'NOIG'),
    ('left', 'MAS', 'MENOS', 'DOSPTS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'UMENOS'),
)


def p_init(p):
    'init : instrucciones'
    p[0] = p[1]


def p_lista_instrucciones(p):
    '''instrucciones : instrucciones instruccion
                     |'''
    if len(p) > 1:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = []


def p_instrucciones_error(p):
    'instrucciones : instrucciones error instruccion'
    p[1].append(p[3])
    p[0] = p[1]


def p_instruccion_declaracion(p):
    '''instruccion : VAR ID DOSPTS tipo_dato IGUAL expresion PTCOMA
                   | CONST ID DOSPTS tipo_dato IGUAL expresion PTCOMA
                   | VAR ID IGUAL expresion PTCOMA
                   | CONST ID IGUAL expresion PTCOMA
                   | VAR ID DOSPTS tipo_dato PTCOMA'''
    params = get_params(p)
    if p[5] == '=':
        p[0] = Declaration(params.line, params.column, p[1], p[2], p[4], p[6])
    elif p[3] == '=':
        p[0] = Declaration(params.line, params.column, p[1], p[2], exp=p[4])
    elif p[5] == ';':
        p[0] = Declaration(params.line, params.column, p[1], p[2], data_type=p[4])


def p_instruccion_asignacion(p):
    'instruccion : acceso IGUAL expresion PTCOMA'
    params = get_params(p)
    p[0] = Assignment(params.line, params.column, p[1], p[3])


def p_instruccion_declaracion_array(p):
    '''instruccion : VAR ID DOSPTS tipo_dato CORIZQ CORDER IGUAL expresion PTCOMA
                   | CONST ID DOSPTS tipo_dato CORIZQ CORDER IGUAL expresion PTCOMA
                   | VAR ID DOSPTS tipo_dato CORIZQ CORDER PTCOMA'''
    params = get_params(p)
    if p[7] == '=':
        p[0] = ArrayDeclaration(params.line, params.column, p[1], p[2], p[4], p[8])
    elif p[7] == ';':
        p[0] = ArrayDeclaration(params.line, params.column, p[1], p[2], p[4])


def p_expresion_array(p):
    '''expresion : CORIZQ lista_expresiones CORDER
                 | CORIZQ CORDER'''
    params = get_params(p)
    if len(p) > 3:
        p[0] = Array(params.line, params.column, p[2])
    else:
        p[0] = Array(params.line, params.column, [])


def p_instruccion_push(p):
    'instruccion : acceso PUNTO PUSH PARIZQ expresion PARDER PTCOMA'
    params = get_params(p)
    p[0] = Push(params.line, params.column, p[1], p[5])


def p_expresion_pop(p):
    'expresion : acceso PUNTO POP PARIZQ PARDER'
    params = get_params(p)
    p[0] = Pop(params.line, params.column, p[1])


def p_expresion_index_of(p):
    'expresion : acceso PUNTO INDEXOF PARIZQ expresion PARDER'
    params = get_params(p)
    p[0] = IndexOf(params.line, params.column, p[1], p[5])


def p_expresion_join(p):
    'expresion : acceso PUNTO JOIN PARIZQ PARDER'
    params = get_params(p)
    p[0] = Join(params.line, params.column, p[1])


def p_expresion_length(p):
    'expresion : acceso PUNTO LENGTH'
    params = get_params(p)
    p[0] = Length(params.line, params.column, p[1])


def p_expresion_acceso(p):
    '''acceso : acceso CORIZQ expresion CORDER
              | acceso PUNTO ID
              | ID'''
    params = get_params(p)
    if len(p) > 4:
        p[0] = ArrayAccess(params.line, params.column, p[1], p[3])
    elif len(p) > 2:
        pass
    else:
        p[0] = Access(params.line, params.column, p[1])


def p_expresion_ternario(p):
    'expresion : expresion INTDER expresion DOSPTS expresion'
    params = get_params(p)
    p[0] = Ternary(params.line, params.column, p[1], p[3], p[5])


def p_instruccion_if(p):
    'instruccion : IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER lista_else_if else'
    params = get_params(p)
    p[0] = If(params.line, params.column, p[3], p[6], p[8], p[9])


def p_lista_else_if(p):
    '''lista_else_if : lista_else_if ELSE IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER
                     |'''
    if len(p) > 1:
        params = get_params(p)
        p[1].append(ElseIf(params.line, params.column, p[5], p[8]))
        p[0] = p[1]
    else:
        p[0] = []


def p_else(p):
    '''else : ELSE LLAVIZQ instrucciones LLAVDER
            |'''
    if len(p) > 1:
        params = get_params(p)
        p[0] = Else(params.line, params.column, p[3])
    else:
        p[0] = None


def p_instruccion_while(p):
    'instruccion : WHILE PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER'
    params = get_params(p)
    p[0] = While(params.line, params.column, p[3], p[6])


def p_instruccion_console_log(p):
    '''instruccion : CONSOLE PUNTO LOG PARIZQ lista_expresiones PARDER PTCOMA
                   | CONSOLE PUNTO LOG PARIZQ PARDER PTCOMA'''
    params = get_params(p)
    if len(p) > 7:
        p[0] = ConsoleLog(params.line, params.column, p[5])
    else:
        p[0] = ConsoleLog(params.line, params.column, [])


def p_lista_expresiones(p):
    '''lista_expresiones : lista_expresiones COMA expresion
                         | expresion'''
    if len(p) > 2:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_expresion_parse_int(p):
    'expresion : PARSEINT PARIZQ expresion PARDER'
    params = get_params(p)
    p[0] = ParseInt(params.line, params.column, p[3])


def p_expresion_parse_float(p):
    'expresion : PARSEFLOAT PARIZQ expresion PARDER'
    params = get_params(p)
    p[0] = ParseFloat(params.line, params.column, p[3])


def p_expresion_to_string(p):
    '''expresion : ENTERO PUNTO TOSTRING PARIZQ PARDER
                 | DECIMAL PUNTO TOSTRING PARIZQ PARDER
                 | TRUE PUNTO TOSTRING PARIZQ PARDER
                 | FALSE PUNTO TOSTRING PARIZQ PARDER
                 | acceso PUNTO TOSTRING PARIZQ PARDER'''
    params = get_params(p)
    p[0] = ToString(params.line, params.column, p[1])


def p_expresion_to_lower_case(p):
    '''expresion : CADENA PUNTO TOLOWERCASE PARIZQ PARDER
                 | acceso PUNTO TOLOWERCASE PARIZQ PARDER'''
    params = get_params(p)
    p[0] = LowerCase(params.line, params.column, p[1])


def p_expresion_to_upper_case(p):
    '''expresion : CADENA PUNTO TOUPPERCASE PARIZQ PARDER
                 | acceso PUNTO TOUPPERCASE PARIZQ PARDER'''
    params = get_params(p)
    p[0] = UpperCase(params.line, params.column, p[1])


def p_expresion_typeof(p):
    'expresion : TYPEOF expresion'
    params = get_params(p)
    p[0] = Typeof(params.line, params.column, p[2])


def p_tipo_dato(p):
    '''tipo_dato : NUMBER
                 | FLOAT
                 | STRING
                 | CHAR
                 | BOOLEAN'''
    if p[1] == 'number':
        p[0] = ExpressionType.NUMBER
    elif p[1] == 'float': 
        p[0] = ExpressionType.FLOAT
    elif p[1] == 'string':
        p[0] = ExpressionType.STRING
    elif p[1] == 'char':
        p[0] = ExpressionType.CHAR
    elif p[1] == 'boolean':
        p[0] = ExpressionType.BOOLEAN


def p_expresion(p):
    '''expresion : ENTERO
                 | DECIMAL
                 | TRUE
                 | FALSE
                 | CADENA
                 | CARACTER
                 | acceso'''
    p[0] = p[1]


def p_expresion_aritmetica(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
                 | expresion MODULO expresion'''
    params = get_params(p)
    if p[2] == '+':
        p[0] = Operation(params.line, params.column, '+', p[1], p[3])
    elif p[2] == '-':
        p[0] = Operation(params.line, params.column, '-', p[1], p[3])
    elif p[2] == '*':
        p[0] = Operation(params.line, params.column, '*', p[1], p[3])
    elif p[2] == '/':
        p[0] = Operation(params.line, params.column, '/', p[1], p[3])
    elif p[2] == '%':
        p[0] = Operation(params.line, params.column, '%', p[1], p[3])


def p_expresion_unaria(p):
    'expresion : MENOS expresion %prec UMENOS'
    params = get_params(p)
    p[0] = Operation(params.line, params.column, '-', p[2])


def p_expresion_agrupacion(p):
    'expresion : PARIZQ expresion PARDER'
    p[0] = p[2]


def p_expresion_relacional(p):
    '''expresion : expresion MAYQUE expresion
                 | expresion MENQUE expresion
                 | expresion MAYIGQUE expresion
                 | expresion MENIGQUE expresion
                 | expresion DOBLEIG expresion
                 | expresion NOIG expresion'''
    params = get_params(p)
    if p[2] == '>':
        p[0] = Operation(params.line, params.column, '>', p[1], p[3])
    elif p[2] == '<':
        p[0] = Operation(params.line, params.column, '<', p[1], p[3])
    elif p[2] == '>=':
        p[0] = Operation(params.line, params.column, '>=', p[1], p[3])
    elif p[2] == '<=':
        p[0] = Operation(params.line, params.column, '<=', p[1], p[3])
    elif p[2] == '==':
        p[0] = Operation(params.line, params.column, '==', p[1], p[3])
    elif p[2] == '!=':
        p[0] = Operation(params.line, params.column, '!=', p[1], p[3])


def p_expresion_logica(p):
    '''expresion : expresion OR expresion
                 | expresion AND expresion
                 | NOT expresion'''
    params = get_params(p)
    if p[2] == '||':
        p[0] = Operation(params.line, params.column, '||', p[1], p[3])
    elif p[2] == '&&':
        p[0] = Operation(params.line, params.column, '&&', p[1], p[3])
    elif p[1] == '!':
        p[0] = Operation(params.line, params.column, '!', p[2])


def p_error(p):
    if p:
        params = get_params(p)
        ast.set_errors(f'No se esperaba el token "{p.type}".', params.line, params.column, 'Sintáctico')
    else:
        ast.set_console('Error sintáctico irrecuperable')
        ast.set_errors(f'Error irrecuperable.', 0, 0, 'Sintáctico')


def get_params(t):
    line = t.lexer.lineno
    lexpos = t.lexpos if isinstance(t.lexpos, int) else 0
    column = lexpos - t.lexer.lexdata.rfind('\n', 0, lexpos) 
    return codeParams(line, column)


class Parser:
    def __init__(self, ast):
        self.ast = ast

    def interpretar(self, input):
        global ast; ast = self.ast
        lexer = lex.lex()
        parser = yacc.yacc()
        result = parser.parse(input)
        return result
