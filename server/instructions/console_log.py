from interfaces.instruction import Instruction
from environment.types import ExpressionType

class ConsoleLog(Instruction):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp

    def ejecutar(self, ast, env):
        output = ''
        for exp in self.exp:
            sym = exp.ejecutar(ast, env)
            if sym.type == ExpressionType.BOOLEAN:
                output += str(sym.value).lower() + ' '
            elif sym.type == ExpressionType.NULL:
                output += 'null '
            else:
                output += str(sym.value) + ' '
        ast.set_console(output)
