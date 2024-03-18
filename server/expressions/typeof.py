from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol

class Typeof(Expression):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp
    
    def ejecutar(self, ast, env):
        sym = self.exp.ejecutar(ast, env)
        if sym.type.name in ['NUMBER', 'FLOAT', 'STRING', 'BOOLEAN', 'CHAR', 'ARRAY', 'NULL']:
            str_type = sym.type.name.lower()
        else:
            str_type = sym.type.name
        return Symbol(self.line, self.col, str_type, ExpressionType.STRING)
