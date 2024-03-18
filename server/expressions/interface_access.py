from interfaces.expression import Expression
from environment.environment import Environment
from environment.types import ExpressionType
from environment.symbol import Symbol

class InterfaceAccess(Expression):
    def __init__(self, line, col, exp, id):
        self.line = line
        self.col = col
        self.exp = exp
        self.id = id

    def ejecutar(self, ast, env):
        sym_interface = self.exp.ejecutar(ast, env)
        env_interface = sym_interface.value

        if not isinstance(env_interface, Environment):
            ast.set_errors(f'"{env_interface}" no es una interface.',
                           self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)

        sym = env_interface.get_variable(ast, self.id, self.line, self.col)
        return sym
