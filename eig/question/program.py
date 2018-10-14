"""
Program structured as a tree.
"""
from enum import Enum

LABELS = {'Water': 0, 'Blue': 1, 'Red': 2, 'Purple': 3}

class ProgramSyntaxError(Exception):
    def __init__(self, program, error_msg="Syntax Error"):
        self.program = program
        self.error_msg = error_msg

    def __str__(self):
        # TODO: Better syntax error message
        return "Error found in the program: \n {} around '{}'".format(self.error_msg, self.program)


class Node:
    def __init__(self, ntype, childs, prog):
        self.ntype = ntype
        self.childs = childs
        self.prog = prog

    def to_dict(self):
        return {'type': self.ntype,
                'childs': [c.to_dict() for c in self.childs]}


class LiteralNode(Node):
    def __init__(self, ntype, value):
        super().__init__(ntype, None, value)
        self.value = value

    def to_dict(self):
        return {'type': self.ntype,
                'value': self.value}


class DataType(Enum):
    ANY = 0
    NUMBER = 1
    BOOLEAN = 2
    COLOR = 3
    LOCATION = 4
    ORIENTATION = 5


class NodeConfig:
    """
    Configs of each kind of node,
    including node type, number of operands, evaluated data type, accepted data type of operands
    """
    def __init__(self, ntype, param_num, dtype, param_dtype):
        self.ntype = ntype
        self.param_num = param_num
        self.dtype = dtype
        self.param_dtype = param_dtype


# mapping from ntype to config
NODES = {
    # basic functions
    'equal': NodeConfig('equal', 2, DataType.BOOLEAN, DataType.ANY),
    'greater': NodeConfig('greater', 2, DataType.BOOLEAN, DataType.NUMBER),
    'less': NodeConfig('less', 2, DataType.BOOLEAN, DataType.NUMBER),
    'plus': NodeConfig('plus', 2, DataType.NUMBER, DataType.NUMBER),
    'minus': NodeConfig('minus', 2, DataType.NUMBER, DataType.NUMBER),
    'and': NodeConfig('and', 2, DataType.BOOLEAN, DataType.BOOLEAN),
    'or': NodeConfig('or', 2, DataType.BOOLEAN, DataType.BOOLEAN),
    'not': NodeConfig('not', 1, DataType.BOOLEAN, DataType.BOOLEAN),

    # board functions
    'color_fn': NodeConfig('color_fn', 1, DataType.COLOR, DataType.LOCATION),
    'orient_fn': NodeConfig('orient_fn', 1, DataType.ORIENTATION, DataType.COLOR),

    # literals
    'number': NodeConfig('number', 0, DataType.NUMBER, None),
    'boolean': NodeConfig('boolean', 0, DataType.BOOLEAN, None),
    'color': NodeConfig('color', 0, DataType.COLOR, None),
    'location': NodeConfig('location', 0, DataType.LOCATION, None),
    'orientation': NodeConfig('orientation', 0, DataType.ORIENTATION, None),
}

# mapping from symbol to ntype for functions
FUNC_NTYPES = {
    # basic functions
    '==': 'equal',
    '>': 'greater',
    '<': 'less',
    '+': 'plus',
    '-': 'minus',
    'and': 'and',
    'or': 'or',
    'not': 'not',

    # board functions
    'color': 'color_fn',
    'orient': 'orient_fn',
}