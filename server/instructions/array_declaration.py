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

    def validate_types(self, array):
        validate = False
        for element in array:
            if not validate:
                if isinstance(element.value, list):
                    validate = self.validate_types(element.value)
                else:
                    if element.type != self.data_type:
                        validate = True
                        break
            else:
                break
        return validate

    def ejecutar(self, ast, env):
        if self.exp:
            result = self.exp.ejecutar(ast, env)
            if result.type != ExpressionType.ARRAY:
                ast.set_errors(f'La expresión "{result.value}" no es un array',
                               self.line, self.col, 'Semántico')
                return
            if self.validate_types(result.value):
                ast.set_errors(f'El array "{self.id}" contiene tipos incorrectos.',
                               self.line, self.col, 'Semántico')
                return
            env.save_variable(ast, self.id, result, self.line, self.col, self.declaration_type)
        else:
            result = Symbol(0, 0, None, ExpressionType.ARRAY)
            env.save_variable(ast, self.id, result, self.line, self.col, self.declaration_type)
