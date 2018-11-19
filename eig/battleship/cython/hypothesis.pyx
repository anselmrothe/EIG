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
    
    def __init__(self, ship_label=None, topleft=None, size=None, orientation=None):
        if (ship_label is None) or (topleft is None) or (size is None) or (orientation is None): return
        self.ship.x = topleft[0]
        self.ship.y = topleft[1]
        self.ship.size = size
        self.ship.label = ship_label
        if orientation == 'H':
            self.ship.orientation = ORIENTATION_HORIZONTAL
        elif orientation == 'V':
            self.ship.orientation = ORIENTATION_VERTICAL

    cdef set_c_ship(self, Ship_c ship):
        self.ship = ship

    @property
    def ship(self):
        return self.ship

    @property
    def ship_label(self):
        return self.ship.label

    @property
    def topleft(self):
        return (self.ship.x, self.ship.y)

    @property
    def size(self):
        return self.ship.size

    @property
    def orientation(self):
        if (self.ship.orientation == ORIENTATION_HORIZONTAL):
            return 'H'
        else:
            return 'V'


cdef class BattleshipHypothesis:

    def __init__(self, grid_size=None, ships=None):
        self.needs_free = False
        if (grid_size is None) or (ships is None): return
        cdef Ship_c* ships_c = array_new[Ship_c](len(ships))
        for i, s in enumerate(ships):
            ships_c[i] = s.ship
        cdef int* board = create_board(grid_size, len(ships), ships_c)
        if board == NULL: raise ValueError 
        self.hypothesis = new Hypothesis(grid_size, grid_size, board, len(ships), ships_c)
        self.needs_free = True

    cdef set_c_hypothesis(self, Hypothesis* hypothesis):
        self.hypothesis = hypothesis

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

    @property
    def ships(self):
        ships = []
        for i in range(self.hypothesis.ship_cnt):
            ship = Ship()
            ship.set_c_ship(self.hypothesis.ships[i])
            ships.append(ship)
        return ships

    def __dealloc__(self):
        if self.needs_free:
            del self.hypothesis


cdef class BattleshipHypothesisSpace:
    cdef vector[Hypothesis*] hypotheses
    cdef int iter_id

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

    def __getitem__(self, x):
        hypothesis = BattleshipHypothesis()
        hypothesis.set_c_hypothesis(self.hypotheses[self.iter_id - 1])
        return hypothesis

    def __iter__(self):
        self.iter_id = 0
        return self

    def __next__(self):
        if self.iter_id >= self.hypotheses.size():
            raise StopIteration
        else:
            
            self.iter_id += 1
            return self.__getitem__(self.iter_id - 1)
    
    def observe(self, observation):
        """
        Given an observation, return a set of ids which hypothesis of that id 
        is consistent with the observation.

        The observation is a numpy array representing a board, where -1 indicates hidden.
        We need to check all locations except -1, and see if the hypothesis agrees with 
        the observation.
        """
        cdef np.ndarray[int, ndim=1, mode="c"] board_c
        cdef vector[int] valid_ids
        board_c = np.ascontiguousarray(observation.flatten(), dtype=ctypes.c_int)
        match_hypotheses_observation(&board_c[0], self.hypotheses, valid_ids)
        return valid_ids

    def execute_on_subspace(self, executor, subset_id):
        cdef Executor _executor = <Executor>executor
        answers = []
        for id in subset_id:
            answers.append(execute_on_hypothesis(_executor, self.hypotheses[id]))
        return answers