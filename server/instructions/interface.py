from interfaces.instruction import Instruction

class Interface(Instruction):
    def __init__(self, line, col, id, attr):
        self.line = line
        self.col = col
        self.id = id
        self.attr = attr

    def ejecutar(self, ast, env):
        if env.id != 'GLOBAL':
            ast.set_errors(f'Declaración incorrecta: interfaz "{self.id}" en el ámbito "{env.id}".',
                           self.line, self.col, 'Semántico')
            return
        for dic in self.attr:
            if self.id == list(dic.values())[0].value:
                ast.set_errors(f'La interfaz "{self.id}" contiene un atributo del mismo tipo.',
                           self.line, self.col, 'Semántico')
                return
        env.save_interface(ast, self.id, self.attr, self.line, self.col)
