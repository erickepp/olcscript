from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol

class ParseFloat(Expression):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp
    
    def ejecutar(self, ast, env):
        sym = self.exp.ejecutar(ast, env)
        if sym.type != ExpressionType.STRING:
            ast.set_errors(f'Tipo de dato incorrecto: "parseFloat({sym.value})".',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
        try:
            return Symbol(self.line, self.col, float(sym.value), ExpressionType.FLOAT)
        except ValueError:
            ast.set_errors(f'No se puede convertir a float: "parseFloat({sym.value})".',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
