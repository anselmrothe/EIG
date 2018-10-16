# distutils: language = c++
# distutils: sources = eig/question/nodes.cc
"""
This is the interface between python and c++ codes.
Here from frontend to backend we have three levels of interaction:
    Python frontend: provide APIs for outside function calls;
    Cython intermediate leval: stores the AST, and translate python objects to c++ types;
    C++ backend: perform the computations.
"""

from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport bool
import ctypes
import numpy as np
cimport numpy as np

from .program import DataType

"""
Declare c++ types to use in this script
"""
cdef extern from "nodes.h":

    cdef const int ORIENTATION_VERTICAL
    cdef const int ORIENTATION_HORIZONTAL

    cdef struct Ship:
        int label, size, orientation, x, y

    cdef cppclass Hypothesis:
        int h, w
        int *board
        Hypothesis()
        Hypothesis(int, int, int*, int, Ship*)

    cdef union value_t:
        int i
        bool b
        int p[2]

    cdef cppclass Node:
        value_t val()
        void evaluate(Hypothesis*, int=-1)

    cdef cppclass FuncNode:
        void add_param(Node*)

    cdef cppclass IntNode:
        void set_val(int)

    cdef cppclass BoolNode:
        void set_val(bool)

    cdef cppclass LocationNode:
        void set_val(short, short)

    Node* build_node(string node_name)
    T* array_new[T](int)

"""
Functions to build AST of c++ classes
"""
cdef Node* build_ast(object question):
    cdef string node_ntype_s = question.ntype.encode('UTF-8')
    cdef Node* node
    node = build_node(node_ntype_s)
    if question.childs:
        node_fn = <FuncNode*> node
        for c in question.childs:
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


cdef class Executor:
    """
    Declare a Cython class to store c++ Node object,
    and as an interface to execute program
    """
    cdef Node* node
    cdef object ret_type

    def __init__(self, question):
        self.node = build_ast(question)
        self.ret_type = question.dtype

    def __dealloc__(self):
        del self.node

    def execute(self, hypothesis):
        cdef int h, w
        cdef np.ndarray[int, ndim=1, mode="c"] board_c
        cdef Ship* ships = array_new[Ship](len(hypothesis.ships))
        h, w = hypothesis.board.shape
        board_c = np.ascontiguousarray(hypothesis.board.flatten(), dtype=ctypes.c_int)
        for i, ship in enumerate(hypothesis.ships):
            ships[i].label = ship.ship_label
            ships[i].size = ship.size
            ships[i].orientation = ORIENTATION_HORIZONTAL if ship.orientation == "horizontal" else ORIENTATION_VERTICAL
            ships[i].x = ship.topleft[0]
            ships[i].y = ship.topleft[1]
        cdef Hypothesis *hypothesis_cpp = new Hypothesis(h, w, &board_c[0], len(hypothesis.ships), ships)

        # perform the computation, and return the result
        self.node.evaluate(hypothesis_cpp)
        cdef value_t result = self.node.val()
        del hypothesis_cpp
        
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