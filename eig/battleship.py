import numpy
from .hypothesis import Hypothesis

class Ship:
    def __init__(self, ship_label, topleft, size, orientation):
        self.topleft = topleft
        self.size = size
        self.orientation = orientation
        self.ship_label = ship_label

class BattleshipHypothesis(Hypothesis):

    def __init__(self, grid_size, ships):
        self.ships = ships
        board = numpy.zeros((grid_size, grid_size))
        for ship in ships:
            # fill in board with ship configurations
            loc = ship.topleft
            board[loc] = ship.ship_label
            if ship.orientation == 'horizontal':
                for _ in range(ship.size - 1):
                    loc = (loc[0], loc[1] + 1)
                    board[loc] = ship.ship_label
            elif ship.orientation == 'vertical':
                for _ in range(ship.size - 1):
                    loc = (loc[0] + 1, loc[1])
                    board[loc] = ship.ship_label
        self.board = board