import numpy
from .hypothesis import Hypothesis


def create_hypothesis_space(grid_size, ships, shipsizes, orientations):
    topleft_positions = [(row, column) for row in range(grid_size)
                         for column in range(grid_size)]
    hypotheses = []
    for ship in ships:
        for shipsize in shipsizes:
            for topleft in topleft_positions:
                for orientation in orientations:
                    hypothesis = BattleshipHypothesis(grid_size=grid_size,
                                                      ship_label=ship,
                                                      topleft=(0, 0), size=2,
                                                      orientation=orientation)
                    hypotheses.append(hypothesis)
    return(hypotheses)


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
