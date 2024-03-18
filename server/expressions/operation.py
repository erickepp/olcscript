from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol
from expressions.primitive import Primitive

class Operation(Expression):
    def __init__(self, line, col, operador, opL, opR=Primitive(0, 0, None, ExpressionType.NULL)):
        self.line = line
        self.col = col
        self.operador = operador
        self.opL = opL
        self.opR = opR

    def get_dominant_type(self, op1, op2):
        if self.operador in ['+', '-', '*', '/', '%']:
            if op1.type == ExpressionType.NUMBER and op2.type == ExpressionType.NUMBER:
                return ExpressionType.NUMBER
            elif op1.type == ExpressionType.NUMBER and op2.type == ExpressionType.FLOAT:
                return ExpressionType.FLOAT
            elif op1.type == ExpressionType.FLOAT and op2.type == ExpressionType.FLOAT:
                return ExpressionType.FLOAT
            elif op1.type == ExpressionType.FLOAT and op2.type == ExpressionType.NUMBER:
                return ExpressionType.FLOAT
            elif op1.type == ExpressionType.STRING and op2.type == ExpressionType.STRING:
                return ExpressionType.STRING
        elif self.operador in ['==', '!=', '>', '>=', '<', '<=']:
            if op1.type == ExpressionType.NUMBER and op2.type == ExpressionType.NUMBER:
                return ExpressionType.BOOLEAN
            elif op1.type == ExpressionType.FLOAT and op2.type == ExpressionType.FLOAT:
                return ExpressionType.BOOLEAN
            elif op1.type == ExpressionType.BOOLEAN and op2.type == ExpressionType.BOOLEAN:
                return ExpressionType.BOOLEAN
            elif op1.type == ExpressionType.STRING and op2.type == ExpressionType.STRING:
                return ExpressionType.BOOLEAN
            elif op1.type == ExpressionType.CHAR and op2.type == ExpressionType.CHAR:
                return ExpressionType.BOOLEAN
        elif self.operador in ['&&', '||']:
            if op1.type == ExpressionType.BOOLEAN and op2.type == ExpressionType.BOOLEAN:
                return ExpressionType.BOOLEAN
        return ExpressionType.NULL
            
    def ejecutar(self, ast, env):
        op1 = self.opL.ejecutar(ast, env)
        op2 = self.opR.ejecutar(ast, env)
        dominant_type = self.get_dominant_type(op1, op2)

        if dominant_type != ExpressionType.NULL:
            if self.operador == '+':
                return Symbol(self.line, self.col, op1.value+op2.value, dominant_type)
            elif self.operador == '-':
                if dominant_type in [ExpressionType.NUMBER, ExpressionType.FLOAT]:
                    return Symbol(self.line, self.col, op1.value-op2.value, dominant_type)
                ast.set_errors(f'Operación incorrecta: "{op1.value} - {op2.value}".',
                               self.line, self.col, 'Semántico')
                return Symbol(0, 0, None, ExpressionType.NULL)
            elif self.operador == '*':
                if dominant_type in [ExpressionType.NUMBER, ExpressionType.FLOAT]:
                    return Symbol(self.line, self.col, op1.value*op2.value, dominant_type)
                ast.set_errors(f'Operación incorrecta: "{op1.value} * {op2.value}".',
                               self.line, self.col, 'Semántico')
                return Symbol(0, 0, None, ExpressionType.NULL)
            elif self.operador == '/':
                if op2.value == 0:
                    ast.set_errors(f'Operación incorrecta: "{op1.value} / 0".',
                                   self.line, self.col, 'Semántico')
                    return Symbol(0, 0, None, ExpressionType.NULL)
                elif dominant_type == ExpressionType.NUMBER:
                    return Symbol(self.line, self.col, int(op1.value/op2.value), dominant_type)
                elif dominant_type == ExpressionType.FLOAT:
                    return Symbol(self.line, self.col, op1.value/op2.value, dominant_type)
                ast.set_errors(f'Operación incorrecta: "{op1.value} / {op2.value}".',
                               self.line, self.col, 'Semántico')
                return Symbol(0, 0, None, ExpressionType.NULL)
            elif self.operador == '%':
                if dominant_type == ExpressionType.NUMBER:
                    return Symbol(self.line, self.col, int(op1.value%op2.value), dominant_type)
                ast.set_errors(f'Operación incorrecta: "{op1.value} % {op2.value}".',
                               self.line, self.col, 'Semántico')
                return Symbol(0, 0, None, ExpressionType.NULL)
            elif self.operador == '==':
                return Symbol(self.line, self.col, op1.value==op2.value, dominant_type)
            elif self.operador == '!=':
                return Symbol(self.line, self.col, op1.value!=op2.value, dominant_type)
            elif self.operador == '>':
                return Symbol(self.line, self.col, op1.value>op2.value, dominant_type)
            elif self.operador == '>=':
                return Symbol(self.line, self.col, op1.value>=op2.value, dominant_type)
            elif self.operador == '<':
                return Symbol(self.line, self.col, op1.value<op2.value, dominant_type)
            elif self.operador == '<=':
                return Symbol(self.line, self.col, op1.value<=op2.value, dominant_type)
            elif self.operador == '&&':
                return Symbol(self.line, self.col, op1.value and op2.value, dominant_type)
            elif self.operador == '||':
                return Symbol(self.line, self.col, op1.value or op2.value, dominant_type)                
        elif op1.type != ExpressionType.NULL and op2.type == ExpressionType.NULL:
            if op1.type in [ExpressionType.NUMBER, ExpressionType.FLOAT] and self.operador == '-':
                return Symbol(self.line, self.col, -op1.value, op1.type)
            elif op1.type == ExpressionType.BOOLEAN and self.operador == '!':
                return Symbol(self.line, self.col, not op1.value, op1.type)
            ast.set_errors(f'Operación incorrecta: "{self.operador}{op1.value}".',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
 
        ast.set_errors(f'Operación incorrecta: "{op1.value} {self.operador} {op2.value}".',
                       self.line, self.col, 'Semántico')
        return Symbol(0, 0, None, ExpressionType.NULL)
