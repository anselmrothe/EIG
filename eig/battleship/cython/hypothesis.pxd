from libcpp cimport bool
from libcpp.vector cimport vector

cdef extern from "hypothesis.h":
    cdef const int ORIENTATION_VERTICAL
    cdef const int ORIENTATION_HORIZONTAL

    cdef struct Ship_c "Ship":
        int label, size, orientation, x, y

    cdef cppclass Hypothesis:
        int h, w, ship_cnt
        int *board
        Ship_c *ships
        Hypothesis()
        Hypothesis(int, int, int*, int, Ship_c*)

    cdef int* create_board(int, int, Ship_c*)
    cdef void create_hypothesis_space(int, vector[int]&, vector[int]&, vector[int]&, vector[Hypothesis*]&)
    cdef void match_hypotheses_observation(int*, vector[Hypothesis*]&, vector[int]&)


cdef class Ship:
    cdef Ship_c ship
    cdef set_c_ship(self, Ship_c ship)


cdef class BattleshipHypothesis:
    cdef int iter_id
    cdef bool needs_free
    cdef Hypothesis* hypothesis
    cdef set_c_hypothesis(self, Hypothesis* hypothesis)
