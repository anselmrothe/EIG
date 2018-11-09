import numpy as np
from itertools import permutations

from ...hypothesis import HypothesisSpace

class Ship:

    def __init__(self, ship_label, topleft, size, orientation):
        self.topleft = topleft
        self.size = size
        self.orientation = orientation
        self.ship_label = ship_label


class BattleshipHypothesis:

    def __init__(self, grid_size, ships):
        self.ships = ships
        self.ship_cnt = len(ships)
        board = np.zeros((grid_size, grid_size))
        for ship in ships:
            # fill in board with ship configurations
            loc = ship.topleft
            if board[loc] > 0: raise ValueError
            board[loc] = ship.ship_label
            if ship.orientation == 'H':
                loc_step = (0, 1)
            elif ship.orientation == 'V':
                loc_step = (1, 0)
            for _ in range(ship.size - 1):
                loc = (loc[0] + loc_step[0], loc[1] + loc_step[1])
                if loc[0] >= grid_size or loc[1] >= grid_size or board[loc] > 0:
                    raise ValueError    
                board[loc] = ship.ship_label
        self.board = board


class BattleshipHypothesisSpace(HypothesisSpace):

    def create_hypothesis_space(self, grid_size, ship_labels, ship_sizes, orientations):
        """
        grid_size: int
        ship_labels, shipsizes, orientations: list
        orientations can only be `V` or `H`
        """
        topleft_positions = [(row, column) for row in range(grid_size)
                            for column in range(grid_size)]
        def ship_generator():
            for topleft in topleft_positions:
                for size in ship_sizes:
                    for orientation in orientations:
                        yield (topleft, size, orientation)
        
        hypotheses = []
        for perm in permutations(ship_generator(), len(ship_labels)):
            ships = []
            for label, config in zip(ship_labels, perm):
                ships.append(Ship(label, *config))
            try:
                hypothesis = BattleshipHypothesis(grid_size, ships)
            except ValueError:
                continue
            hypotheses.append(hypothesis)
        return hypotheses

    def match(self, i, observation):
        """
        The observation is a numpy array representing a board, where -1 indicates hidden.
        We need to check all locations except -1, and see if the hypothesis agrees with 
        the observation.
        """
        # both hypothesis.board and observation are numpy arrays, so we can use element-wise 
        # logical operations in numpy to efficiently compare them.
        hypothesis = self.hypotheses[i].board
        return np.all(np.logical_or(observation < 0, np.equal(hypothesis, observation)))

    def execute_on_subspace(self, executor, subset_id):
        answers = []
        for id in subset_id:
            answers.append(executor.execute(self.hypotheses[id]))
        return answers