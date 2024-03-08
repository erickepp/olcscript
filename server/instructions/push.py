from interfaces.instruction import Instruction
from environment.types import ExpressionType

class Push(Instruction):
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
            return
        if sym.value is None:
            ast.set_errors(f'La variable "{self.array.id}" no tiene un array asignado.',
                           self.line, self.col, 'Semántico')
            return
        element = self.exp.ejecutar(ast, env)
        sym.value.append(element)
