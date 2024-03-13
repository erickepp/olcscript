from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.types import ExpressionType
from environment.execute import statement_executer

class If(Instruction):
    def __init__(self, line, col, exp, block, else_if_list, else_instruction):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block
        self.else_if_list = else_if_list
        self.else_instruction = else_instruction

    def ejecutar(self, ast, env):
        validate = self.exp.ejecutar(ast, env)
        if validate.type != ExpressionType.BOOLEAN:
            ast.set_errors(f'Expresión incorrecta: "{validate.value} no es boolean".',
                            self.line, self.col, 'Semántico')
            return
        
        if validate.value:
            if_env = Environment(env, 'IF')
            statement_executer(self.block, ast, if_env)
            return

        for else_if in self.else_if_list:
            if else_if.ejecutar(ast, env):
                return
        
        if self.else_instruction:
            self.else_instruction.ejecutar(ast, env)
