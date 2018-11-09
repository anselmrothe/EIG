# distutils: language = c++
# distutils: sources = eig/battleship/cpp/hypothesis.cc
"""
This is the interface between python and c++ codes.
In this module, we provide a class which implement all attributes of HypothesisSpace
    and leave all the real calculation work to c++.
"""

from libcpp.string cimport string
from libcpp.vector cimport vector
import ctypes
import numpy as np
cimport numpy as np


"""
Declare c++ types to use in this script
"""
from .hypothesis cimport *
from .executor cimport Executor, array_new


cdef object execute_on_hypothesis(Executor executor, Hypothesis* h):
    return executor.execute_c(h)


cdef class Ship:
    
    def __init__(self, ship_label, topleft, size, orientation):
        self.ship.x = topleft[0]
        self.ship.y = topleft[1]
        self.ship.size = size
        self.ship.label = ship_label
        if orientation == 'H':
            self.ship.orientation = ORIENTATION_HORIZONTAL
        elif orientation == 'V':
            self.ship.orientation = ORIENTATION_VERTICAL

    @property
    def ship(self):
        return self.ship


cdef class BattleshipHypothesis:

    def __init__(self, grid_size, ships):
        cdef Ship_c* ships_c = array_new[Ship_c](len(ships))
        for i, s in enumerate(ships):
            ships_c[i] = s.ship
        cdef int* board = create_board(grid_size, len(ships), ships_c)
        if board == NULL: raise ValueError 
        self.hypothesis = new Hypothesis(grid_size, grid_size, board, len(ships), ships_c)

    @property
    def board(self):
        # package as a numpy array
        cdef int grid_size = self.hypothesis.h, i
        board = []
        for i in range(grid_size * grid_size):
            board.append(self.hypothesis.board[i])
        return np.array(board).reshape((grid_size, grid_size))

    @property
    def ship_cnt(self):
        return self.hypothesis.ship_cnt

    def __dealloc__(self):
        del self.hypothesis


cdef class BattleshipHypothesisSpace:
    cdef vector[Hypothesis*] hypotheses

    def __init__(self, grid_size, ship_labels, ship_sizes, orientations):
        # package parameters into vectors
        cdef vector[int] ship_labels_vec, ship_sizes_vec, orientations_vec
        for elem in ship_labels: ship_labels_vec.push_back(elem)
        for elem in ship_sizes: ship_sizes_vec.push_back(elem)
        for elem in orientations:
            if elem == 'V': orientations_vec.push_back(ORIENTATION_VERTICAL)
            elif elem == 'H': orientations_vec.push_back(ORIENTATION_HORIZONTAL)
            else:
                raise ValueError("Orientation can only be 'V' or 'H'")
        create_hypothesis_space(grid_size, ship_labels_vec, ship_sizes_vec, orientations_vec, self.hypotheses)

    def __dealloc__(self):
        cdef Hypothesis* h
        for h in self.hypotheses:
            del h

    def __len__(self):
        return self.hypotheses.size()
    
    def observe(self, observation):
        """
        Given an observation, return a set of ids which hypothesis of that id 
        is not consistent with the observation.

        The observation is a numpy array representing a board, where -1 indicates hidden.
        We need to check all locations except -1, and see if the hypothesis agrees with 
        the observation.
        """
        cdef np.ndarray[int, ndim=1, mode="c"] board_c
        cdef vector[int] except_ids
        board_c = np.ascontiguousarray(observation.flatten(), dtype=ctypes.c_int)
        match_hypotheses_observation(&board_c[0], self.hypotheses, except_ids)
        return set(except_ids)

    def execute_on_subspace(self, executor, subset_id):
        cdef Executor _executor = <Executor>executor
        answers = []
        for id in subset_id:
            answers.append(execute_on_hypothesis(_executor, self.hypotheses[id]))
        return answers