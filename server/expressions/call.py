from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType
from environment.environment import Environment
from environment.execute import statement_executer

class Call(Expression):
    def __init__(self, line, col, id, params):
        self.line = line
        self.col = col
        self.id = id
        self.params = params

    def ejecutar(self, ast, env):
        func = env.get_function(ast, self.id, self.line, self.col)

        if func == {}:
            return

        if len(self.params) != len(func['params']):
            ast.set_errors(f'La función "{self.id}" esperaba {len(func['params'])} parámetros, \
                           pero se obtuvieron {len(self.params)}.', self.line, self.col, 'Semántico')
            return Symbol(0, 0, None, ExpressionType.NULL)

        function_env = Environment(env.get_global_environment(), f'FUNCTION_{self.id}')

        for i in range(len(self.params)):
            sym_param = self.params[i].ejecutar(ast, env)

            id_param = list(func['params'][i].keys())[0]
            type_param = list(func['params'][i].values())[0]

            if type_param.value != sym_param.type.value:
                ast.set_errors(f'Los tipos de parámetros de la función "{self.id}" son incorrectos.',
                               self.line, self.col, 'Semántico')
                return Symbol(0, 0, None, ExpressionType.NULL)

            function_env.save_variable(ast, id_param, sym_param, self.line, self.col, 'var')

        return_value = statement_executer(func['block'], ast, function_env)

        if return_value:
            if return_value.value.type.value != func['type'].value:
                ast.set_errors(f'El tipo de retorno de la función "{self.id}" es incorrecto.',
                               self.line, self.col, 'Semántico')
                return Symbol(0, 0, None, ExpressionType.NULL)
            return return_value.value
        return Symbol(0, 0, None, ExpressionType.NULL)
