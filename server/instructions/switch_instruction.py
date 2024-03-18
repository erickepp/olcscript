from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.types import ExpressionType
from environment.execute import statement_executer

class Switch(Instruction):
    def __init__(self, line, col, exp, case_list, default_instruction):
        self.line = line
        self.col = col
        self.exp = exp
        self.case_list = case_list
        self.default_instruction = default_instruction

    def ejecutar(self, ast, env):
        switch_exp = self.exp.ejecutar(ast, env)
        switch_env = Environment(env, 'SWITCH_CASE')
        flag_case = False

        for case in self.case_list:
            case_exp = case.exp.ejecutar(ast, switch_env)

            if switch_exp.type != case_exp.type:
                ast.set_errors('Los tipos de dato no son iguales.',
                               case.line, case.col, 'Semántico')
                return

            if switch_exp.value == case_exp.value or flag_case:
                flag_case = True
                return_value = statement_executer(case.block, ast, switch_env)
                if return_value:
                    if return_value.type == ExpressionType.BREAK:
                        return
                    return return_value
        
        if self.default_instruction:
            switch_env = Environment(env, 'SWITCH_DEFAULT')
            return_value = statement_executer(self.default_instruction.block, ast, switch_env)
            if return_value:
                if return_value.type == ExpressionType.BREAK:
                    return
                return return_value
        

class Case:
    def __init__(self, line, col, exp, block):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block


class Default:
    def __init__(self, line, col, block):
        self.line = line
        self.col = col
        self.block = block
