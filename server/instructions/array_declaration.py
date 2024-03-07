from interfaces.instruction import Instruction
from environment.symbol import Symbol
from environment.types import ExpressionType

class ArrayDeclaration(Instruction):
    def __init__(self, line, col, declaration_type, id, data_type, exp=None):
        self.line = line
        self.col = col
        self.declaration_type = declaration_type
        self.id = id
        self.data_type = data_type
        self.exp = exp

    def ejecutar(self, ast, env):
        if self.exp:
            result = self.exp.ejecutar(ast, env)
            for res in result.value:
                if res.type != self.data_type:
                    ast.set_errors(f'El array "{self.id}" contiene tipos incorrectos.',
                                   self.line, self.col, 'Semántico')
                    return
            env.save_variable(ast, self.id, result, self.line, self.col, self.declaration_type)
        else:
            result = Symbol(0, 0, None, ExpressionType.ARRAY)
            env.save_variable(ast, self.id, result, self.line, self.col, self.declaration_type)
