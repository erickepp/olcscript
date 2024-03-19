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
            ast.set_symbols(id, 'Variable', symbol.type.name, self.id, line)
        elif declaration_type == 'const':
            self.constants[id] = symbol
            ast.set_symbols(id, 'Constante', symbol.type.name, self.id, line)

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
                elif symbol.type.value != tmp_env.tabla[id].type.value:
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

    def save_interface(self, ast, id, interface, line, col):
        if id in self.interfaces:
            ast.set_errors(f'Ya existe una interface con el nombre "{id}".', line, col, 'Semántico')
            return
        self.interfaces[id] = interface
        ast.set_symbols(id, 'Interfaz', '', self.id, line)
    
    def get_interface(self, ast, id, line, col):
        tmp_env = self
        while True:
            if id in tmp_env.interfaces:
                return tmp_env.interfaces[id]
            if tmp_env.previous == None:
                break
            else:
                tmp_env = tmp_env.previous
        ast.set_errors(f'La interfaz "{id}" no está definida.', line, col, 'Semántico')

    def save_function(self, ast, id, function, line, col):
        if id in self.functions:
            ast.set_errors(f'Ya existe una función con el nombre "{id}".', line, col, 'Semántico')
            return
        self.functions[id] = function
        ast.set_symbols(id, 'Función', function['type'].name, self.id, line)

    def get_function(self, ast, id, line, col):
        tmp_env = self
        while True:
            if id in tmp_env.functions:
                return tmp_env.functions[id]
            if tmp_env.previous == None:
                break
            else:
                tmp_env = tmp_env.previous
        ast.set_errors(f'La función "{id}" no está definida.', line, col, 'Semántico')
        return {}

    def switch_validation(self):
        tmpEnv = self
        while True:
            if tmpEnv.id in ['SWITCH_CASE', 'SWITCH_DEFAULT']:
                return True
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        return False

    def loop_validation(self):
        tmpEnv = self
        while True:
            if tmpEnv.id in ['WHILE', 'FOR']:
                return True
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        return False
