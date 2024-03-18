from interfaces.expression import Expression
from environment.environment import Environment
from environment.symbol import Symbol
from environment.types import ExpressionType

class Object(Expression):
    def __init__(self, line, col, func, exp):
        self.line = line
        self.col = col
        self.func = func
        self.exp = exp
    
    def ejecutar(self, ast, env):
        sym_interface = self.exp.ejecutar(ast, env)
        env_interface = sym_interface.value

        if not isinstance(env_interface, Environment):
            return Symbol(0, 0, None, ExpressionType.NULL)
        
        array = Symbol(self.line, self.col, [], ExpressionType.ARRAY)

        if self.func == 'keys':
            for key in env_interface.tabla.keys():
                array.value.append(Symbol(0, 0, key, ExpressionType.STRING))
        elif self.func == 'values':
            for value in env_interface.tabla.values():
                array.value.append(Symbol(0, 0, str(value.value), ExpressionType.STRING))

        return array
        