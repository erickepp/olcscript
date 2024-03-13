from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType

class Break(Expression):
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def ejecutar(self, ast, env):
        if env.id in ['SWITCH_CASE', 'SWITCH_DEFAULT'] or env.loop_validation():
            return Symbol(self.line, self.col, None, ExpressionType.BREAK)
        ast.set_errors('"break" no se encuentra dentro de un bloque "switch", "while" o "for".',
                       self.line, self.col, 'Semántico')
        return Symbol(self.line, self.col, None, ExpressionType.NULL)
