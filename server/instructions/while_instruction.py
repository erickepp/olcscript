from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.types import ExpressionType
from environment.execute import statement_executer

class While(Instruction):
    def __init__(self, line, col, exp, block):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block

    def ejecutar(self, ast, env):
        result = self.exp.ejecutar(ast, env)
        if result.type != ExpressionType.BOOLEAN:
            ast.set_errors(f'Expresión incorrecta: "{result.value} no es boolean".',
                            self.line, self.col, 'Semántico')
            return
        
        safe_cont = 0
        while True:
            safe_cont += 1
            result = self.exp.ejecutar(ast, env)
            if result.value:
                while_env = Environment(env, 'WHILE')
                while_env.tabla.clear()
                while_env.constants.clear()
                flag = statement_executer(self.block, ast, while_env)
                if flag:
                    if flag.type == ExpressionType.BREAK:
                        break
                    elif flag.type == ExpressionType.CONTINUE:
                        continue
                    elif flag.type == ExpressionType.RETURN:
                        return flag
            else:
                break
            if safe_cont >= 1000:
                ast.set_errors('Se ha excedido el máximo de ciclos permitidos.',
                               self.line, self.col, 'Semántico')
                break
