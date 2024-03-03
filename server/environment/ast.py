class Ast:
    def __init__(self):
        self.instructions = []
        self.console = ''
        self.errors = []

    def set_console(self, content):
        self.console += content + '\n'
    
    def get_console(self):
        return self.console.encode().decode('unicode_escape')

    def add_instructions(self, instructions):
        self.instructions += instructions
    
    def get_instructions(self):
        return self.instructions
    
    def set_errors(self, description, line, col, type):
        self.errors.append({
            'description': description,
            'line': line,
            'col': col,
            'type': type
        })
    
    def get_errors(self):
        return self.errors
