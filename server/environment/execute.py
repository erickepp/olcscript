from environment.types import ExpressionType

def root_executer(instruction_list, ast, env):
    for inst in instruction_list or []:
        inst.ejecutar(ast, env)

def statement_executer(instruction_list, ast, env):
    for inst in instruction_list:
        res = inst.ejecutar(ast, env)
        if res and res.type != ExpressionType.NULL:
            return res
    return None
