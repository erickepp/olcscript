from interfaces.instruction import Instruction
from environment.types import ExpressionType

class Decrement(Instruction):
    def __init__(self, line, col, access, exp):
        self.line = line
        self.col = col
        self.access = access
        self.exp = exp
    
    def ejecutar(self, ast, env):
        sym = self.access.ejecutar(ast, env)
        if sym.type not in [ExpressionType.NUMBER, ExpressionType.FLOAT]:
            ast.set_errors(f'No se puede usar "+=" con el tipo de dato "{sym.type.name.lower()}"',
                           self.line, self.col, 'Semántico')
            return

        result = self.exp.ejecutar(ast, env)
        if result.type != sym.type and result.type != ExpressionType.NUMBER:
            ast.set_errors('Los tipos de dato no son iguales.', self.line, self.col, 'Semántico')
            return

        sym.value -= result.value
