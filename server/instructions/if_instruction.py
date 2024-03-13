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
        if_exp = self.exp.ejecutar(ast, env)
        if if_exp.type != ExpressionType.BOOLEAN:
            ast.set_errors(f'Expresión incorrecta: "{if_exp.value} no es boolean".',
                            self.line, self.col, 'Semántico')
            return
        if if_exp.value:
            if_env = Environment(env, 'IF')
            return_value = statement_executer(self.block, ast, if_env)
            return return_value

        else_if_env = Environment(env, 'ELSE_IF')
        for else_if in self.else_if_list:
            else_if_exp = else_if.exp.ejecutar(ast, env)
            if else_if_exp.type != ExpressionType.BOOLEAN:
                ast.set_errors(f'Expresión incorrecta: "{else_if_exp.value} no es boolean".',
                                else_if.line, else_if.col, 'Semántico')
                return
            if else_if_exp.value:
                return_value = statement_executer(else_if.block, ast, else_if_env)
                return return_value
        
        if self.else_instruction:
            else_env = Environment(env, 'ELSE')
            return_value = statement_executer(self.else_instruction.block, ast, else_env)
            return return_value


class ElseIf:
    def __init__(self, line, col, exp, block):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block


class Else:
    def __init__(self, line, col, block):
        self.line = line
        self.col = col
        self.block = block
