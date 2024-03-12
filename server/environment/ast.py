class Ast:
    def __init__(self):
        self.instructions = []
        self.console = ''
        self.errors = []
        self.symbols = []

    def set_console(self, content):
        self.console += content + '\n'
    
    def get_console(self):
        return self.console.encode('latin1').decode('unicode_escape')

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
    
    def set_symbols(self, id, symbol_type, data_type, scope, line):
        self.symbols.append({
            'id': id,
            'symbolType': symbol_type,
            'dataType': data_type,
            'scope': scope,
            'line': line
        })

    def get_symbols(self):
        new_symbols = []
        seen_pairs = set()
        for symbol in self.symbols:
            tuple_symbol = tuple(symbol.items())
            if tuple_symbol not in seen_pairs:
                seen_pairs.add(tuple_symbol)
                new_symbols.append(symbol)
        return new_symbols
