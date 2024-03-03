from environment.symbol import Symbol
from environment.types import ExpressionType

class Environment:
    def __init__(self, previous, id):
        self.previous = previous
        self.id = id
        self.tabla = {}
        self.interfaces = {}
        self.functions = {}

    def save_variable(self, ast, id, symbol, line, col):
        if id in self.tabla:
            ast.setErrors(f'La variable "{id}" ya existe.', line, col, 'Semántico')
            return
        self.tabla[id] = symbol

    def get_variable(self, ast, id, line, col):
        tmp_env = self
        while True:
            if id in tmp_env.tabla:
                return tmp_env.tabla[id]
            if tmp_env.previous == None:
                break
            else:
                tmp_env = tmp_env.previous
        ast.set_errors(f'La variable "{id}" no existe', line, col, 'Semántico')
        return Symbol(0, 0, None, ExpressionType.NULL)

    def set_variable(self, ast, id, symbol, line, col):
        tmp_env = self
        while True:
            if id in tmp_env.tabla:
                tmp_env.tabla[id] = symbol
                return symbol
            if tmp_env.previous == None:
                break
            else:
                tmp_env = tmp_env.previous
        ast.set_errors(f'La variable "{id}" no existe', line, col, 'Semántico')
        return Symbol(0, 0, None, ExpressionType.NULL)
