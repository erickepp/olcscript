from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.symbol import Symbol
from environment.types import InterfaceType

class InterfaceDeclaration(Instruction):
    def __init__(self, line, col, declaration_type, id1, id2, content):
        self.line = line
        self.col = col
        self.declaration_type = declaration_type
        self.id1 = id1
        self.id2 = id2
        self.content = content

    def ejecutar(self, ast, env):
        interface_value = env.get_interface(ast, self.id2, self.line, self.col)

        if interface_value is None:
            return

        new_env = Environment(None, f'INTERFACE_{self.id2}')

        for i in range(len(self.content)):
            id_param = list(interface_value[i].keys())[0]
            type_param = list(interface_value[i].values())[0]

            id_exp = list(self.content[i].keys())[0]
            val_exp = list(self.content[i].values())[0].ejecutar(ast, env)

            if type_param.value == val_exp.type.value and id_param == id_exp:
                new_env.save_variable(ast, id_param, val_exp, self.line, self.col, 'var')
            else:
                ast.set_errors('El tipo o identificador de la interfaz es incorrecto.',
                               self.line, self.col, 'Semántico')
                return

        sym = Symbol(self.line, self.col, new_env, InterfaceType(self.id2))
        env.save_variable(ast, self.id1, sym, self.line, self.col, self.declaration_type)
