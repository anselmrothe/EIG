"""
Program structured as a tree.
"""
from enum import Enum

LABELS = {'Water': 0, 'Blue': 1, 'Red': 2, 'Purple': 3}

class NodeConfig:
    """
    Configs of each kind of node,
    including node type, number of parameters, evaluated data type, accepted data type of parameters

    params_dtypes accepts two formats:
    a tuple (e.g. (DataType.NUMBER, ) or (DataType.LAMBDA_X, DataType.BOOLEAN)), whose length is 1 or the same
            as number of params, means types of params must be exactly in correspondance of types in the tuple.
            Length 1 means all parameters have the same type;
    a list of tuples (e.g. [(DataType.LAMBDA_FXB, DataType.SET_B), (DataType.LAMBDA_FXN, DataType.SET_N)]) 
            means the combination of params types can be any of the tuples in the list.

    dtype also accepts two formats:
    a single DataType object, means this function always evaluates to this type;
    a list of DataType objects. This can only be used when params_dtypes is a list, and the length of this tuple
            should be the same with param_dtypes. This means the evaluted type is determined by type of paramters.
            The i-th combination of paramters in list param_dtype will result in the i-th type in list dtype.
    """
    def __init__(self, ntype, param_num, dtype, param_dtypes):
        self.ntype = ntype
        self.param_num = param_num
        self.dtype = dtype
        self.param_dtypes = param_dtypes


class DataType(Enum):
    NUMBER = 1
    BOOLEAN = 2
    COLOR = 3
    LOCATION = 4
    ORIENTATION = 5
    LAMBDA_X = 6
    LAMBDA_Y = 7
    LAMBDA_FXB = 8
    LAMBDA_FYB = 9
    LAMBDA_FXN = 10
    LAMBDA_FXL = 11
    SET_S = 12
    SET_B = 13
    SET_N = 14
    SET_L = 15


# mapping from ntype to config
NODES = {
    # basic functions
    'equal': NodeConfig('equal', 2, DataType.BOOLEAN, [(DataType.BOOLEAN, ), (DataType.NUMBER, ), 
                                        (DataType.COLOR, ), (DataType.LOCATION, ), (DataType.ORIENTATION, )]),
    'set_equal': NodeConfig('set_equal', 1, DataType.BOOLEAN, (DataType.SET_N, )),
    'greater': NodeConfig('greater', 2, DataType.BOOLEAN, (DataType.NUMBER, )),
    'less': NodeConfig('less', 2, DataType.BOOLEAN, (DataType.NUMBER, )),
    'plus': NodeConfig('plus', 2, DataType.NUMBER, [(DataType.NUMBER, ), (DataType.BOOLEAN, )]),
    'minus': NodeConfig('minus', 2, DataType.NUMBER, (DataType.NUMBER, )),
    'sum_op': NodeConfig('sum_op', 1, DataType.NUMBER, [(DataType.SET_N, ), (DataType.SET_B, )]),
    'and_op': NodeConfig('and_op', 2, DataType.BOOLEAN, (DataType.BOOLEAN, )),
    'or_op': NodeConfig('or_op', 2, DataType.BOOLEAN, (DataType.BOOLEAN, )),
    'not_op': NodeConfig('not_op', 1, DataType.BOOLEAN, (DataType.BOOLEAN, )),
    'row': NodeConfig('row', 1, DataType.NUMBER, (DataType.LOCATION, )),
    'col': NodeConfig('col', 1, DataType.NUMBER, (DataType.LOCATION, )),
    'topleft': NodeConfig('topleft', 1, DataType.LOCATION, (DataType.SET_L, )),
    'bottomright': NodeConfig('bottomright', 1, DataType.LOCATION, (DataType.SET_L, )),
    'set_size': NodeConfig('set_size', 1, DataType.NUMBER, (DataType.SET_L, )),
    'is_subset': NodeConfig('is_subset', 2, DataType.BOOLEAN, (DataType.SET_L, )),

    # board functions
    'color_fn': NodeConfig('color_fn', 1, DataType.COLOR, (DataType.LOCATION, )),
    'orient_fn': NodeConfig('orient_fn', 1, DataType.ORIENTATION, (DataType.COLOR, )),
    'touch_fn': NodeConfig('touch_fn', 2, DataType.BOOLEAN, (DataType.COLOR, )),
    'size_fn': NodeConfig('size_fn', 1, DataType.NUMBER, (DataType.COLOR, )),
    'colored_tiles_fn': NodeConfig('colored_tiles_fn', 1, DataType.SET_L, (DataType.COLOR, )),

    # set functions
    'any_op': NodeConfig('any_op', 1, DataType.BOOLEAN, (DataType.SET_B, )),
    'all_op': NodeConfig('all_op', 1, DataType.BOOLEAN, (DataType.SET_B, )),
    'map_op': NodeConfig('map_op', 2, [DataType.SET_B, DataType.SET_B, DataType.SET_L, DataType.SET_N], 
                    [(DataType.LAMBDA_FXB, DataType.SET_S), (DataType.LAMBDA_FYB, DataType.SET_L),
                     (DataType.LAMBDA_FXL, DataType.SET_S), (DataType.LAMBDA_FXN, DataType.SET_S)]),
    'set_op': NodeConfig('set_op', -1, [DataType.SET_L, DataType.SET_L, DataType.SET_S, DataType.SET_S], 
                    [(DataType.SET_L, ), (DataType.LOCATION, ), (DataType.SET_S, ), (DataType.COLOR, )]),
    'set_diff': NodeConfig('set_diff', 2, DataType.SET_L, (DataType.SET_L, )),
    'union': NodeConfig('union', 2, DataType.SET_L, (DataType.SET_L, )),
    'intersect': NodeConfig('intersect', 2, DataType.SET_L, (DataType.SET_L, )),
    'unique': NodeConfig('unique', 1, DataType.SET_L, (DataType.SET_L, )),
    'lambda_op': NodeConfig('lambda_op', 2, [DataType.LAMBDA_FXB, DataType.LAMBDA_FXL, DataType.LAMBDA_FXN, DataType.LAMBDA_FYB], 
                    [(DataType.LAMBDA_X, DataType.BOOLEAN), (DataType.LAMBDA_X, DataType.LOCATION),
                     (DataType.LAMBDA_X, DataType.NUMBER), (DataType.LAMBDA_Y, DataType.BOOLEAN)]),

    # literals
    'number': NodeConfig('number', 0, DataType.NUMBER, None),
    'boolean': NodeConfig('boolean', 0, DataType.BOOLEAN, None),
    'color': NodeConfig('color', 0, DataType.COLOR, None),
    'location': NodeConfig('location', 0, DataType.LOCATION, None),
    'orientation': NodeConfig('orientation', 0, DataType.ORIENTATION, None),
    'lambda_x': NodeConfig('lambda_x', 0, DataType.LAMBDA_X, None),
    'lambda_y': NodeConfig('lambda_y', 0, DataType.LAMBDA_Y, None),
    'set_color': NodeConfig('set_color', 0, DataType.SET_S, None),
    'set_location': NodeConfig('set_location', 0, DataType.SET_L, None)
}

# mapping from symbol to ntype for functions
FUNC_NTYPES = {
    # basic functions
    '==': 'equal',
    '===': 'set_equal',
    '>': 'greater',
    '<': 'less',
    '+': 'plus',
    '-': 'minus',
    '++': 'sum_op',
    'and': 'and_op',
    'or': 'or_op',
    'not': 'not_op',
    'rowL': 'row',
    'colL': 'col',

    # board functions
    'color': 'color_fn',
    'orient': 'orient_fn',
    'touch': 'touch_fn',
    'size': 'size_fn',
    'coloredTiles': 'colored_tiles_fn',

    # set functions
    'any': 'any_op',
    'all': 'all_op',
    'map': 'map_op',
    'set': 'set_op',
    'topleft': 'topleft',
    'bottomright': 'bottomright',
    'setSize': 'set_size',
    'isSubset': 'is_subset',
    'setDifference': 'set_diff',
    'union': 'union',
    'intersection': 'intersect',
    'unique': 'unique',
    'lambda': 'lambda_op',
}

class ProgramSyntaxError(Exception):
    def __init__(self, program, error_msg="Syntax Error"):
        self.program = program
        self.error_msg = error_msg

    def __str__(self):
        # TODO: Better program error location suggestion
        # maybe raise a location during recursive parsing, and package the real exception at top level
        return "Error found in the program: \n {} around '{}'".format(self.error_msg, self.program)


class Node:
    def __init__(self, ntype, children, prog):
        self.ntype = ntype
        self.children = children
        self.prog = prog

    def to_dict(self):
        return {'type': self.ntype,
                'children': [c.to_dict() for c in self.children]}


class LiteralNode(Node):
    def __init__(self, ntype, value, prog=None):
        super().__init__(ntype, None, prog or value)
        self.value = value

    def to_dict(self):
        return {'type': self.ntype,
                'value': self.value}


class LambdaVarNode(Node):
    def __init__(self, var, value):
        super().__init__('lambda_{}'.format(var), None, value)
        self.value = value
    
    def to_dict(self):
        return {'type': self.ntype,
                'value': self.value}
