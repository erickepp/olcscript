from interfaces.instruction import Instruction
from environment.types import ExpressionType
from environment.symbol import Symbol

class Array(Instruction):
    def __init__(self, line, col, list_exp):
        self.line = line
        self.col = col
        self.list_exp = list_exp

    def ejecutar(self, ast, env):
        arr_val = []
        for exp in self.list_exp:
            index_exp = exp.ejecutar(ast, env)
            arr_val.append(index_exp)
        return Symbol(self.line, self.col, arr_val, ExpressionType.ARRAY)
