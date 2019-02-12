from ..program import DataType, LambdaVarNode
from . import functions as F

class Executor:
    def __init__(self, question):
        self._executor = self._build_executor(question)

    def _traverse_ast(self, hypothesis, node, **lambda_args):
        # for leaf nodes, return its value 
        if node.children is None:
            if isinstance(node, LambdaVarNode):
                return lambda_args[node.value]
            else: return node.value
        
        # for lambdas, return a wrapper function 
        if node.ntype == "lambda_op":
            def lambda_f(var):
                lambda_args[node.children[0].value] = var
                return self._traverse_ast(hypothesis, node.children[1], **lambda_args)
            return lambda_f 

        # for other functions, evaluate its arguments first, and execute the function
        arguments = []
        if node.ntype.endswith("_fn"):
            # first argument of board functions is the hypothesis
            arguments.append(hypothesis)
        for c in node.children:
            arguments.append(self._traverse_ast(hypothesis, c, **lambda_args))
        # call the function and return its result
        return getattr(F, node.ntype)(node, *arguments)

    def _build_executor(self, question):
        def f(hypothesis):
            return self._traverse_ast(hypothesis, question)
        return f

    def execute(self, hypothesis):
        return self._executor(hypothesis)