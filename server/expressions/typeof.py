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
        str_type = sym.type.name.lower()
        return Symbol(self.line, self.col, str_type, ExpressionType.STRING)
