from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.execute import statement_executer

class Else(Instruction):
    def __init__(self, line, col, block):
        self.line = line
        self.col = col
        self.block = block

    def ejecutar(self, ast, env):
        else_env = Environment(env, 'ELSE')
        statement_executer(self.block, ast, else_env)
