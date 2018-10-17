import re
from .program import *

class Parser:

    @staticmethod
    def parse(program : str):
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
        
        return ast

    @staticmethod
    def parse_literal(token: str):
        if token in {'x', 'y'}:
            return LambdaVarNode(token)
        elif token in {'H', 'V'}:
            return LiteralNode('orientation', token)
        elif token in {'FALSE', 'TRUE'}:
            return LiteralNode('boolean', token == 'TRUE')
        elif token in LABELS:
            return LiteralNode('color', LABELS[token])
        elif token.isdigit():
            return LiteralNode('number', int(token))
        else:
            match = re.fullmatch(r'(\d)-(\d)', token)
            if match:
                location = (int(match.group(1)) - 1, int(match.group(2)) - 1)
                return LiteralNode('location', location)
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
            raise ProgramSyntaxError(' '.join(program), 'Unrecognized function name')
        
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

        childs = [Parser.recursive_parse(prog) for prog in subprograms]
        return Node(func_ntype, childs, ' '.join(program))

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
        if node.childs is None:
            node.dtype = NODES[node.ntype].dtype
            if node.ntype in {'lambda_x', 'lambda_y'} and (in_lambda is not None):
                if not node.dtype == in_lambda:
                    raise ProgramSyntaxError(node.prog, 
                        "{} should not exist in lambda expression of {}".format(node.dtype, in_lambda))
                if node.dtype == DataType.LAMBDA_X:
                    node.dtype = DataType.COLOR
                if node.dtype == DataType.LAMBDA_Y:
                    node.dtype = DataType.LOCATION
            return
        
        if node.ntype == 'lambda':
            if in_lambda:
                # TODO: consider allow nested lambda functions
                # This can be achieved by a symbol table, which contains different lambda variables and their bindings.
                raise ProgramSyntaxError(node.prog, "Nested Lambda function is not allowed.")
            Parser.type_check(node.childs[0])
            Parser.type_check(node.childs[1], in_lambda=node.childs[0].dtype)
        else:
            for c in node.childs:
                Parser.type_check(c, in_lambda)
                
        param_dtypes = tuple(c.dtype for c in node.childs)
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