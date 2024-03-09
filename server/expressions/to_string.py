from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol

class ToString(Expression):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp
    
    def ejecutar(self, ast, env):
        sym = self.exp.ejecutar(ast, env)

        if sym.type in [ExpressionType.NUMBER, ExpressionType.FLOAT]:
            return Symbol(self.line, self.col, str(sym.value), ExpressionType.STRING)
        elif sym.type == ExpressionType.BOOLEAN:
            str_value = str(sym.value).lower()
            return Symbol(self.line, self.col, str_value, ExpressionType.STRING)
        else:
            ast.set_errors(f'Tipo de dato incorrecto: "{sym.value}.toString()".',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
