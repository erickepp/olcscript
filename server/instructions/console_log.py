from interfaces.instruction import Instruction
from environment.types import ExpressionType

class ConsoleLog(Instruction):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp

    def get_str_array(self, array):
        str_array = []
        for element in array:
            if isinstance(element.value, list):
                str_array.append(self.get_str_array(element.value))
            else:
                str_array.append(str(element.value))
        return f'[{', '.join(str_array)}]'

    def ejecutar(self, ast, env):
        output = ''
        for exp in self.exp:
            sym = exp.ejecutar(ast, env)
            if sym.type == ExpressionType.BOOLEAN:
                output += str(sym.value).lower() + ' '
            elif sym.type == ExpressionType.NULL:
                output += 'null '
            elif sym.type == ExpressionType.ARRAY:
                if sym.value is not None:
                    output += self.get_str_array(sym.value) + ' '
                else:
                    output += 'null '
            else:
                output += str(sym.value) + ' '
        ast.set_console(output)
