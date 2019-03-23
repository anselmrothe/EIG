import re
from .program import *
from .python.executor import Executor

class Parser:

    @staticmethod
    def parse(program : str, optimization=False):
        # tokenize the program
        tokens = program.replace('(', ' ( ').replace(')', ' ) ').split()
        try:
            ast = Parser.recursive_parse(tokens)
        except ProgramSyntaxError:
            raise
        except Exception:
            raise ProgramSyntaxError(program)

        # perform type checks
        Parser.type_check(ast)
        top_type = ast.dtype
        if top_type not in {DataType.BOOLEAN, DataType.NUMBER, 
            DataType.LOCATION, DataType.COLOR, DataType.ORIENTATION}:
            raise ProgramSyntaxError(program, "Top level type cannot be {}".format(top_type))

        if optimization:
            ast, _ = Parser.optimize(ast)
        
        return ast

    @staticmethod
    def parse_literal(token: str):
        # first match lambda
        lambda_match = re.fullmatch(r'(x|y)\d+', token)
        if lambda_match is not None:
            return LambdaVarNode(lambda_match.group(1), lambda_match.group(0))
        elif token in {'H', 'V'}:
            return LiteralNode('orientation', token)
        elif token in {'FALSE', 'TRUE'}:
            return LiteralNode('boolean', token == 'TRUE', token)
        elif token in LABELS:
            return LiteralNode('color', LABELS[token], token)
        elif token.isdigit():
            return LiteralNode('number', int(token), token)
        elif token == 'AllColors':
            return LiteralNode('set_color', token)
        elif token == 'AllTiles':
            return LiteralNode('set_location', token)
        else:
            match = re.fullmatch(r'(\d)-(\d)', token)
            if match:
                location = (int(match.group(1)) - 1, int(match.group(2)) - 1)
                return LiteralNode('location', location, token)
            else:
                raise ProgramSyntaxError(token, 'Unrecognized token')
    
    @staticmethod
    def parse_function(program : list):
        # find function information
        func_symbol = program[0]
        if func_symbol in FUNC_NTYPES:
            func_ntype = FUNC_NTYPES[func_symbol]
            func_config = NODES[func_ntype]
            param_num = func_config.param_num
        else:
            raise ProgramSyntaxError(' '.join(program), 'Unrecognized function name "{}"'.format(func_symbol))
        
        # parse parameters first
        subprograms = []
        start_func = -1
        in_func_level = 0
        for idx in range(1, len(program)):
            if program[idx] == '(':
                if in_func_level == 0:
                    in_func_level = 1
                    start_func = idx
                else:
                    in_func_level += 1
            elif program[idx] == ')':
                if in_func_level == 0:
                    raise ProgramSyntaxError(' '.join(program[idx:]), 'Parentheses matching error.')
                else:
                    in_func_level -= 1
                    if in_func_level == 0:
                        if start_func + 1 == idx:
                            raise ProgramSyntaxError(program[start_func: idx + 1])
                        subprograms.append(program[start_func: idx + 1])    
            elif in_func_level == 0:
                # single token
                subprograms.append([program[idx]])
        
        # check if parameter number is correct
        if param_num >= 0 and (not len(subprograms) == param_num):
            raise ProgramSyntaxError(' '.join(program),
                'Operand number mismatch. {} expected, found {}'.format(param_num, len(subprograms)))

        children = [Parser.recursive_parse(prog) for prog in subprograms]
        return Node(func_ntype, children, ' '.join(program))

    @staticmethod
    def recursive_parse(program : list):
        if len(program) == 1:                            # parse as a literal
            return Parser.parse_literal(program[0])
        elif program[0] == '(' and program[-1] == ')':   # parse as a program
            return Parser.parse_function(program[1:-1])
        else:
            raise ProgramSyntaxError(' '.join(program))

    @staticmethod
    def type_check_tuple(accepted_dtypes : tuple, param_dtypes : tuple):
        if len(accepted_dtypes) == 1:
            atype = accepted_dtypes[0]
            for i, ptype in enumerate(param_dtypes):
                if not (ptype == atype):
                    return (atype, i + 1, ptype)
        else:
            for i, (atype, ptype) in enumerate(zip(accepted_dtypes, param_dtypes)):
                if not (atype == ptype):
                    return (atype, i + 1, ptype)
        return True

    @staticmethod
    def type_check(node : Node, in_lambda=None):
        """
        Bottom-up type check pass.
        in_lambda means currently in the lambda function body
        """
        if node.children is None:
            # constants or lambda variable
            node.dtype = NODES[node.ntype].dtype
            if isinstance(node, LambdaVarNode) and (in_lambda is not None):
                if node.value not in in_lambda:
                    raise ProgramSyntaxError(node.prog, "Lambda variable {} should not exist here".format(node.value))
                if node.dtype == DataType.LAMBDA_X:
                    node.dtype = DataType.COLOR
                if node.dtype == DataType.LAMBDA_Y:
                    node.dtype = DataType.LOCATION
            return
        
        # process children
        if node.ntype == 'lambda_op':
            if in_lambda is None: in_lambda = []
            if not isinstance(node.children[0], LambdaVarNode):
                raise ProgramSyntaxError(node.prog, "Parameter type mismatch. "
                    "The first child of lambda operator should be lambda\n"
                    "variable (x0, x1, y2, etc.), get {}".format(str(node.children[0].ntype)))
            var = node.children[0].value
            if var in in_lambda:
                raise ProgramSyntaxError(node.prog, "Lambda variable {} has already been defined".format(var))
            Parser.type_check(node.children[0])
            Parser.type_check(node.children[1], in_lambda + [var])
        else:
            for c in node.children:
                Parser.type_check(c, in_lambda)
        
        # perform type check of current node
        param_dtypes = tuple(c.dtype for c in node.children)
        accepted_dtypes = NODES[node.ntype].param_dtypes
        eval_dtypes = NODES[node.ntype].dtype

        if isinstance(accepted_dtypes, tuple):
            check_res = Parser.type_check_tuple(accepted_dtypes, param_dtypes)
            if check_res is not True:
                raise ProgramSyntaxError(node.prog, "Parameter type mismatch. "
                        "Expected {} for parameter {}, get {}".format(*check_res))
            else:
                node.dtype = eval_dtypes

        elif isinstance(accepted_dtypes, list):
            eval_type = None
            for i, types in enumerate(accepted_dtypes):
                if Parser.type_check_tuple(types, param_dtypes) is True: 
                    if isinstance(eval_dtypes, list):
                        eval_type = eval_dtypes[i]
                    else: eval_type = eval_dtypes
                    break
            if not eval_type:
                expected_types = ",\n  ".join([Parser.param_types_str(types) for types in accepted_dtypes])
                raise ProgramSyntaxError(node.prog, "Parameter type mismatch. "
                    "Expected one of\n  {},\nget {}".format(expected_types, Parser.param_types_str(param_dtypes)))
            node.dtype = eval_type

    @staticmethod
    def param_types_str(types : tuple):
        return "({})".format(", ".join([str(t) for t in types]))

    @staticmethod
    def optimize(node: Node):
        """
        Optimize the program by constant deduction.
        Returns:
            node (Node): optimized syntax tree
            is_const (bool): whether the subprogram represented by this node is constant
        """
        # leafs
        if node.children is None:
            return node, not isinstance(node, LambdaVarNode)
        
        # intermediate nodes
        is_and = (node.ntype == 'and_op')
        is_or = (node.ntype == 'or_op')
        can_optimize = True
        for i, c in enumerate(node.children):
            if node.ntype == 'lambda_op' and i == 0: continue   # for lambda, we only care about its body
            cnode, is_const = Parser.optimize(c)
            if is_const:
                node.children[i] = cnode
            else:
                # for most intermediate nodes, optimization is allowed only if all arguments are constant
                can_optimize = False
            if is_const and (is_and or is_or):
                # for logical expressions, use special trick
                if is_and and (not cnode.value):
                    bool_node = LiteralNode('boolean', False, node.prog)
                    bool_node.dtype = node.dtype
                    return bool_node, True
                if is_or and cnode.value:
                    bool_node = LiteralNode('boolean', True, node.prog)
                    bool_node.dtype = node.dtype
                    return bool_node, True

        if node.ntype.endswith('_fn'):
            # value for board functions cannot be deduced
            return node, False

        if can_optimize:
            e = Executor(node)
            value = e.execute(None)
            if node.dtype == DataType.NUMBER: ntype = 'number'
            elif node.dtype == DataType.BOOLEAN: ntype = 'boolean'
            elif node.dtype == DataType.COLOR: ntype = 'color'
            elif node.dtype == DataType.LOCATION: ntype = 'location'
            elif node.dtype == DataType.ORIENTATION: ntype = 'orientation'
            else:
                if node.ntype == 'map_op':
                # if the body of its lambda function is constant, then 
                # map function can be optimized as a set of consts
                    if node.dtype == DataType.SET_B: item_ntype = 'boolean'
                    elif node.dtype == DataType.SET_L: item_ntype = 'location'
                    elif node.dtype == DataType.SET_N: item_ntype = 'number'
                    children = []
                    for item in value:
                        children.append(LiteralNode(item_ntype, item))
                    set_node = Node('set_op', children, node.prog)
                    set_node.dtype = node.dtype
                    return set_node, True
                return node, True
                
            const_node = LiteralNode(ntype, value, node.prog)
            const_node.dtype = node.dtype
            return const_node, True
        else: return node, False