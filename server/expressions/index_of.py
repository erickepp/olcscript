from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol

class IndexOf(Expression):
    def __init__(self, line, col, array, exp):
        self.line = line
        self.col = col
        self.array = array
        self.exp = exp

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
        element = self.exp.ejecutar(ast, env)
        arr = [element.value for element in sym.value]
        try:
            index = arr.index(element.value)
            return Symbol(0, 0, index, ExpressionType.NUMBER)
        except ValueError:
            return Symbol(0, 0, -1, ExpressionType.NUMBER)
