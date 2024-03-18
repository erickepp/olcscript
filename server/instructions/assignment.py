from interfaces.instruction import Instruction
from expressions.access import Access
from expressions.array_access import ArrayAccess
from expressions.interface_access import InterfaceAccess
from environment.types import ExpressionType

class Assignment(Instruction):
    def __init__(self, line, col, id, exp):
        self.line = line
        self.col = col
        self.id = id
        self.exp = exp

    def ejecutar(self, ast, env):
        if isinstance(self.id, Access):
            result = self.exp.ejecutar(ast, env)
            env.set_variable(ast, self.id.id, result, self.line, self.col)
        elif isinstance(self.id, ArrayAccess) or isinstance(self.id, InterfaceAccess):
            sym = self.id.ejecutar(ast, env)
            if sym.type == ExpressionType.NULL:
                return
            result = self.exp.ejecutar(ast, env)
            if sym.type.value != result.type.value:
                ast.set_errors('Asignación incorrecta: tipos de dato diferentes.',
                            self.line, self.col, 'Semántico')
                return
            sym.value = result.value
