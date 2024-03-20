from enum import Enum

class ExpressionType(Enum):
    NUMBER = 0
    FLOAT = 1
    STRING = 2
    BOOLEAN = 3
    CHAR = 4
    ARRAY = 5
    NULL = 6
    BREAK = 7
    CONTINUE = 8
    RETURN = 9

class InterfaceType:
    def __init__(self, value):
        self.value = value
        self.name = value
