# distutils: language = c++
# distutils: sources = eig/battleship/cpp/nodes.cc
"""
This is the interface between python and c++ codes.
Here from frontend to backend we have three levels of interaction:
    Python frontend: provide APIs for outside function calls;
    Cython intermediate leval: stores the AST, and translate python objects to c++ types;
    C++ backend: perform the computations.
"""

from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.unordered_map cimport unordered_map
from libcpp cimport bool
import ctypes
import numpy as np
cimport numpy as np

from ..program import DataType, LambdaVarNode

"""
Declare c++ types to use in this script
"""
from executor cimport *
from .hypothesis cimport BattleshipHypothesis

"""
Functions to build AST of c++ classes
"""
cdef Node* build_ast(object question):
    cdef string node_ntype_s = question.ntype.encode('UTF-8')
    cdef Node* node
    node = build_node(node_ntype_s)
    node.set_name(node_ntype_s)
    if isinstance(question, LambdaVarNode):
        lambda_var_name = question.value.encode('UTF-8')
        node.set_name(lambda_var_name)
    if question.children:
        node_fn = <FuncNode*> node
        for c in question.children:
            node_c = build_ast(c)
            node_fn.add_param(node_c)
    else:
        setup_literal_node(question, node_ntype_s, node)
    return node

cdef Node* setup_literal_node(object node_py, string node_ntype_s, Node* node_cpp):
    cdef int i, x, y
    cdef bool b
    if node_ntype_s == "number" or node_ntype_s == "color":
        i = node_py.value
        (<IntNode*>node_cpp).set_val(i)
    elif node_ntype_s == "boolean":
        b = node_py.value
        (<BoolNode*>node_cpp).set_val(b)
    elif node_ntype_s == "location":
        x = node_py.value[0]
        y = node_py.value[1]
        (<LocationNode*>node_cpp).set_val(x, y)
    elif node_ntype_s == "orientation":
        if node_py.value == "V":
            (<IntNode*>node_cpp).set_val(ORIENTATION_VERTICAL)
        else:
            (<IntNode*>node_cpp).set_val(ORIENTATION_HORIZONTAL)
    elif node_ntype_s == "set_color":
        (<IntNode*>node_cpp).set_val(SET_COLORS)
    elif node_ntype_s == "set_location":
        (<IntNode*>node_cpp).set_val(SET_LOCATIONS)


cdef class Executor:
    """
    Declare a Cython class to store c++ Node object,
    and as an interface to execute program
    """
    def __init__(self, question):
        self.node = build_ast(question)
        self.ret_type = question.dtype

    def __dealloc__(self):
        del self.node

    cdef object execute_c(self, Hypothesis* hypothesis):
        cdef unordered_map[string, int] lambda_args
        self.node.evaluate(hypothesis, lambda_args)
        cdef value_t result = self.node.val()
        # return w.r.t top-level type
        if self.ret_type == DataType.NUMBER or self.ret_type == DataType.COLOR:
            return result.i
        elif self.ret_type == DataType.BOOLEAN:
            return result.b
        elif self.ret_type == DataType.LOCATION:
            return (result.p[0], result.p[1])
        elif self.ret_type == DataType.ORIENTATION:
            if (result.i == ORIENTATION_VERTICAL): return "V"
            elif (result.i == ORIENTATION_HORIZONTAL): return "H"

    cdef object execute_cy(self, BattleshipHypothesis hypothesis):
        return self.execute_c(hypothesis.hypothesis)

    def execute(self, hypothesis):
        if not hasattr(hypothesis, "ships"):
            # a cython class
            return self.execute_cy(hypothesis)

        cdef int h, w
        cdef np.ndarray[int, ndim=1, mode="c"] board_c
        cdef Ship* ships = array_new[Ship](len(hypothesis.ships))
        h, w = hypothesis.board.shape
        board_c = np.ascontiguousarray(hypothesis.board.flatten(), dtype=ctypes.c_int)
        for i, ship in enumerate(hypothesis.ships):
            ships[i].label = ship.ship_label
            ships[i].size = ship.size
            ships[i].orientation = ORIENTATION_HORIZONTAL if ship.orientation == "H" else ORIENTATION_VERTICAL
            ships[i].x = ship.topleft[0]
            ships[i].y = ship.topleft[1]
        cdef Hypothesis *hypothesis_cpp = new Hypothesis(h, w, &board_c[0], len(hypothesis.ships), ships)

        # perform the computation, and return the result
        result = self.execute_c(hypothesis_cpp)
        del hypothesis_cpp
        return result