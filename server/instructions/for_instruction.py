from interfaces.instruction import Instruction
from instructions.declaration import Declaration
from environment.environment import Environment
from environment.types import ExpressionType
from environment.execute import statement_executer

class For(Instruction):
    def __init__(self, line, col, id1, exp1, exp2, id2, block):
        self.line = line
        self.col = col
        self.id1= id1
        self.exp1 = exp1
        self.exp2 = exp2
        self.id2 = id2
        self.block = block
    
    def ejecutar(self, ast, env):
        for_env = Environment(env, 'FOR')
        declaration = Declaration(self.line, self.col, 'var', self.id1,
                           ExpressionType.NUMBER, self.exp1)
        declaration.ejecutar(ast, for_env)

        result = self.exp2.ejecutar(ast, for_env)
        if result.type != ExpressionType.BOOLEAN:
            ast.set_errors(f'Expresión incorrecta: "{result.value} no es boolean".',
                            self.line, self.col, 'Semántico')
            return
        
        sym = for_env.get_variable(ast, self.id2, self.line, self.col)
        if sym.type != ExpressionType.NUMBER:
            ast.set_errors(f'Expresión incorrecta: "{sym.value} no es number".',
                            self.line, self.col, 'Semántico')
            return
        
        while result.value:
            for_env.tabla = dict([next(iter(for_env.tabla.items()))])
            for_env.constants.clear()
            
            flag = statement_executer(self.block, ast, for_env)
            if flag:
                if flag.type == ExpressionType.BREAK:
                    break
                elif flag.type == ExpressionType.CONTINUE:
                    pass
                elif flag.type == ExpressionType.RETURN:
                    return flag

            sym.value += 1
            result = self.exp2.ejecutar(ast, for_env)
