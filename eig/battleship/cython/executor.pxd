from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.unordered_map cimport unordered_map
from libcpp cimport bool
from .hypothesis cimport BattleshipHypothesis

cdef extern from "hypothesis.h":
    cdef const int ORIENTATION_VERTICAL
    cdef const int ORIENTATION_HORIZONTAL
    cdef const int SET_COLORS
    cdef const int SET_LOCATIONS

    cdef struct Ship:
        int label, size, orientation, x, y

    cdef cppclass Hypothesis:
        int h, w
        int *board
        Hypothesis()
        Hypothesis(int, int, int*, int, Ship*)

cdef extern from "nodes.h":
    cdef union value_t:
        int i
        bool b
        int p[2]

    cdef cppclass Node:
        value_t val()
        void evaluate(Hypothesis*, unordered_map[string, int]&) except +RuntimeError
        void set_name(string)

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


cdef class Executor:
    """
    Declare a Cython class to store c++ Node object,
    and as an interface to execute program
    """
    cdef Node* node
    cdef object ret_type

    cdef object execute_c(self, Hypothesis* hypothesis)
    cdef object execute_cy(self, BattleshipHypothesis hypothesis)
