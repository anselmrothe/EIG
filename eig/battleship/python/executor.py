# TODO: Reimplement a python version executor
class Executor:
    def __init__(self, question):
        self._executor = self._build_executor(question)

    def _build_executor(self, question):
        raise NotImplementedError()

    def execute(self, hypothesis):
        raise NotImplementedError()