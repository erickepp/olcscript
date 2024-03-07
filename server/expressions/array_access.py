from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol

class ArrayAccess(Expression):
    def __init__(self, line, col, array, index):
        self.line = line
        self.col = col
        self.array = array
        self.index = index

    def ejecutar(self, ast, env):
        sym = self.array.ejecutar(ast, env)
        if sym.type != ExpressionType.ARRAY:
            ast.set_errors(f'La variable "{self.array.id}" no es un array.',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
        index_val = self.index.ejecutar(ast, env)
        if index_val.type != ExpressionType.NUMBER:
            ast.set_errors(f'Índice incorrecto: "{self.array.id}[{index_val.value}]."',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
        if index_val.value < 0 or index_val.value >= len(sym.value):
            ast.set_errors(f'Índice de array "{self.array.id}" fuera de rango.',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)
        return sym.value[index_val.value]
