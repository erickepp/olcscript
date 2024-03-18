from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType

class Continue(Expression):
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def ejecutar(self, ast, env):
        if env.loop_validation():
            return Symbol(self.line, self.col, None, ExpressionType.CONTINUE)
        ast.set_errors('"continue" no se encuentra dentro de un bloque "while" o "for".',
                       self.line, self.col, 'Semántico')
        return Symbol(0, 0, None, ExpressionType.NULL)
