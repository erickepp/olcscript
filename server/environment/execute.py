def root_executer(instruction_list, ast, env):
    for inst in instruction_list or []:
        inst.ejecutar(ast, env)

def statement_executer(instruction_list, ast, env):
    for inst in instruction_list:
        res = inst.ejecutar(ast, env)
        if res is not None:
            return res
    return None
