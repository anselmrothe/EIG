from .parser import Parser
from .program import ProgramSyntaxError
#TODO: cpp version?
from .python.priors import EqualSizesDistribution
import traceback

try:
    from .cython.executor import Executor
    from .cython.hypothesis import *
except ImportError:
    print("Error import cython")
    traceback.print_exc()
    from .python.executor import Executor
    from .python.hypothesis import *