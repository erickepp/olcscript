from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.types import ExpressionType
from environment.execute import statement_executer

class ElseIf(Instruction):
    def __init__(self, line, col, exp, block):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block

    def ejecutar(self, ast, env):
        validate = self.exp.ejecutar(ast, env)
        if validate.type != ExpressionType.BOOLEAN:
            ast.set_errors(f'Expresión incorrecta: "{validate.value} no es boolean".',
                            self.line, self.col, 'Semántico')
            return
        if validate.value:
            else_if_env = Environment(env, 'ELSE_IF')
            statement_executer(self.block, ast, else_if_env)
            return True
