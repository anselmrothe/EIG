import re
from .program import *

class Parser:

    @staticmethod
    def parse(program : str):
        # tokenize the program
        tokens = program.replace('(', ' ( ').replace(')', ' ) ').split()
        ast = Parser.recursive_parse(tokens)
        Parser.type_check(ast)
        return ast

    @staticmethod
    def parse_literal(token: str):
        # TODO: deal with lambda variables
        if token in {'H', 'V'}:
            return LiteralNode('orientation', token)
        if token in LABELS:
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
                        subprograms.append(program[start_func: idx + 1])    
            elif in_func_level == 0:
                # single token
                subprograms.append([program[idx]])
        
        # check if parameter number is correct
        if not len(subprograms) == param_num:
            raise ProgramSyntaxError(' '.join(program),
                'Operand number mismatch. {} expected, found {}'.format(param_num, len(subprograms)))

        childs = [Parser.recursive_parse(prog) for prog in subprograms]
        return Node(func_ntype, childs, ' '.join(program))

    @staticmethod
    def recursive_parse(program : list):
        # TODO: support lambda expression
        if len(program) == 1:                            # parse as a literal
            return Parser.parse_literal(program[0])
        elif program[0] == '(' and program[-1] == ')':   # parse as a program
            return Parser.parse_function(program[1:-1])
        else:
            raise ProgramSyntaxError(' '.join(program))

    @staticmethod
    def type_check(node : Node):
        """
        A simple type check pass.
        """
        if node.childs is None: return
        accepted_dtype = NODES[node.ntype].param_dtype
        for c in node.childs:
            dtype = NODES[c.ntype].dtype
            if accepted_dtype == DataType.ANY or accepted_dtype == dtype:
                Parser.type_check(c)
            else:
                raise ProgramSyntaxError(node.prog, "Parameter type mismatch")
