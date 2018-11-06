from .parser import Parser

try:
    from .cython.executor import Executor
    from .cython.hypothesis import *
except ImportError:
    from .python.executor import Executor
    from .python.hypothesis import *