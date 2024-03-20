from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType

class Return(Expression):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp

    def ejecutar(self, ast, env):
        if env.function_validation():
            if self.exp is None:
                return Symbol(self.line, self.col, Symbol(0, 0, None, ExpressionType.NULL),
                              ExpressionType.RETURN)
            sym = self.exp.ejecutar(ast, env)
            return Symbol(self.line, self.col, sym, ExpressionType.RETURN)
        ast.set_errors('"return" no se encuentra dentro de una función.', self.line, self.col, 'Semántico')
        return Symbol(0, 0, None, ExpressionType.NULL)
