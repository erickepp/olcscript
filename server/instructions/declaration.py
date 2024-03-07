from interfaces.instruction import Instruction
from environment.symbol import Symbol
from environment.types import ExpressionType

class Declaration(Instruction):
    def __init__(self, line, col, declaration_type, id, data_type=None, exp=None):
        self.line = line
        self.col = col
        self.declaration_type = declaration_type
        self.id = id
        self.data_type = data_type
        self.exp = exp

    def ejecutar(self, ast, env):
        if self.data_type and self.exp:
            result = self.exp.ejecutar(ast, env)
            if result.type == ExpressionType.NUMBER and self.data_type == ExpressionType.FLOAT:
                result.value = float(result.value)
                result.type = self.data_type
            elif result.type != self.data_type:
                ast.set_errors(f'Declaración incorrecta: \
                               "{self.id}: {self.data_type.name.lower()} = {result.value}"',
                               self.line, self.col, 'Semántico')
                return
            env.save_variable(ast, self.id, result, self.line, self.col, self.declaration_type)
        elif self.data_type is None and self.exp:
            result = self.exp.ejecutar(ast, env)
            env.save_variable(ast, self.id, result, self.line, self.col, self.declaration_type)
        elif self.data_type and self.exp is None:
            if self.data_type == ExpressionType.NUMBER:
                value = 0
            elif self.data_type == ExpressionType.FLOAT:
                value = 0.0
            elif self.data_type in [ExpressionType.STRING, ExpressionType.CHAR]:
                value = ''
            elif self.data_type == ExpressionType.BOOLEAN:
                value = True
            result = Symbol(0, 0, value, self.data_type)
            env.save_variable(ast, self.id, result, self.line, self.col, self.declaration_type)
