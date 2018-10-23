# TODO: remove this and python version when cython version of hypothesis is finished
USE_CYTHON = True
if USE_CYTHON:
    from .hypothesis_cy import *
else:
    from .hypothesis_py import *
