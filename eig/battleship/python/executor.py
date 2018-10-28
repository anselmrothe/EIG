from ..program import DataType
from . import functions as F

class Executor:
    def __init__(self, question):
        self._executor = self._build_executor(question)

    def _traverse_ast(self, hypothesis, node, lambda_v=None):
        arguments = []
        if node.ntype.endswith("_fn"):
            arguments.append(hypothesis)
        if node.childs is None:
            if node.ntype.startswith("lambda_"):
                return lambda_v
            else: return node.value
        if node.ntype == "lambda_op":
            def lambda_f(x):
                return self._traverse_ast(hypothesis, node.childs[1], x)
            return lambda_f 
        for c in node.childs:
            arguments.append(self._traverse_ast(hypothesis, c, lambda_v))
        return getattr(F, node.ntype)(*arguments)

    def _build_executor(self, question):
        def f(hypothesis):
            return self._traverse_ast(hypothesis, question)
        return f

    def execute(self, hypothesis):
        return self._executor(hypothesis)