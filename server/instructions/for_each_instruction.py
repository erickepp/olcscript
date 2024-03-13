from interfaces.instruction import Instruction
from instructions.declaration import Declaration
from expressions.primitive import Primitive
from environment.environment import Environment
from environment.types import ExpressionType
from environment.execute import statement_executer

class ForEach(Instruction):
    def __init__(self, line, col, id, array, block):
        self.line = line
        self.col = col
        self.id= id
        self.array = array
        self.block = block
    
    def ejecutar(self, ast, env):
        array_sym = self.array.ejecutar(ast, env)
        if array_sym.type != ExpressionType.ARRAY:
                ast.set_errors(f'La expresión "{array_sym.value}" no es un array',
                               self.line, self.col, 'Semántico')
                return
        if array_sym.value is None:
             return
        
        for_env = Environment(env, 'FOR')
        for sym in array_sym.value:
            for_env.tabla.clear()
            for_env.constants.clear()

            primitive = Primitive(sym.line, sym.col, sym.value, sym.type)
            declaration = Declaration(self.line, self.col, 'const', self.id, exp=primitive)
            declaration.ejecutar(ast, for_env)
            
            flag = statement_executer(self.block, ast, for_env)
            if flag:
                if flag.type == ExpressionType.BREAK:
                    break
                elif flag.type == ExpressionType.CONTINUE:
                    continue
