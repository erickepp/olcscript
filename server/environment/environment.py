from environment.symbol import Symbol
from environment.types import ExpressionType

class Environment:
    def __init__(self, previous, id):
        self.previous = previous
        self.id = id
        self.tabla = {}
        self.constants = {}
        self.interfaces = {}
        self.functions = {}

    def save_variable(self, ast, id, symbol, line, col, declaration_type):
        if id in self.tabla or id in self.constants:
            ast.set_errors(f'La variable "{id}" ya existe.', line, col, 'Semántico')
            return
        elif symbol.type == ExpressionType.NULL:
            ast.set_errors(f'Declaración incorrecta: "{id} = null".', line, col, 'Semántico')
            return
        if declaration_type == 'var':
            self.tabla[id] = symbol
        elif declaration_type == 'const':
            self.constants[id] = symbol

    def get_variable(self, ast, id, line, col):
        tmp_env = self
        while True:
            if id in tmp_env.tabla:
                return tmp_env.tabla[id]
            elif id in tmp_env.constants:
                return tmp_env.constants[id]
            if tmp_env.previous == None:
                break
            else:
                tmp_env = tmp_env.previous
        ast.set_errors(f'La variable "{id}" no está definida.', line, col, 'Semántico')
        return Symbol(0, 0, None, ExpressionType.NULL)

    def set_variable(self, ast, id, symbol, line, col):
        tmp_env = self
        while True:
            if id in tmp_env.tabla:
                if symbol.type == ExpressionType.NUMBER and tmp_env.tabla[id].type == ExpressionType.FLOAT:
                    symbol.value = float(symbol.value)
                    symbol.type = ExpressionType.FLOAT
                elif symbol.type != tmp_env.tabla[id].type:
                    ast.set_errors(f'Asignación incorrecta: \
                                   "{id}: {tmp_env.tabla[id].type.name.lower()} = {symbol.value}"',
                                   line, col, 'Semántico')
                    return
                tmp_env.tabla[id] = symbol
                return symbol
            elif id in tmp_env.constants:
                ast.set_errors(f'No se puede modificar la constante "{id}".' ,line, col, 'Semántico')
                return
            if tmp_env.previous == None:
                break
            else:
                tmp_env = tmp_env.previous
        ast.set_errors(f'La variable "{id}" no está definida.', line, col, 'Semántico')
        return Symbol(0, 0, None, ExpressionType.NULL)
