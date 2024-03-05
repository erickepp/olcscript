from interfaces.instruction import Instruction
from environment.types import ExpressionType

class Assignment(Instruction):
    def __init__(self, line, col, id, exp):
        self.line = line
        self.col = col
        self.id = id
        self.exp = exp

    def ejecutar(self, ast, env):
        result = self.exp.ejecutar(ast, env)
        env.set_variable(ast, self.id, result, self.line, self.col)
