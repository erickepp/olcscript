from interfaces.instruction import Instruction

class Function(Instruction):
    def __init__(self, line, col, id, params, type, block):
        self.line = line
        self.col = col
        self.id = id
        self.params = params
        self.type = type
        self.block = block

    def ejecutar(self, ast, env):
        if env.id != 'GLOBAL':
            ast.set_errors(f'Declaración incorrecta: función "{self.id}" en el ámbito "{env.id}".',
                           self.line, self.col, 'Semántico')
            return
        function_data = {
            'params': self.params,
            'type': self.type,
            'block': self.block
        }
        env.save_function(ast, self.id, function_data, self.line, self.col)
