from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol

class Length(Expression):
    def __init__(self, line, col, array):
        self.line = line
        self.col = col
        self.array = array

    def ejecutar(self, ast, env):
        sym = self.array.ejecutar(ast, env)
        if sym.type != ExpressionType.ARRAY:
            ast.set_errors(f'La variable "{self.array.id}" no es un array.',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
        if sym.value is None:
            ast.set_errors(f'La variable "{self.array.id}" no tiene un array asignado.',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
        length = len(sym.value)
        return Symbol(self.line, self.col, length, ExpressionType.NUMBER)
