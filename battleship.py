import numpy
import unittest
from hypothesis import Hypothesis

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


class Test(unittest.TestCase):

    def test_hypothesis(self):
        ships = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='vertical'),
                       Ship(ship_label=2, topleft=(0, 1), size=2, orientation='horizontal')]
        hypothesis = BattleshipHypothesis(grid_size=3, ships=ships)
        
        board = numpy.array([1, 2, 2, 1, 0, 0, 1, 0, 0]).reshape(3, 3)
        self.assertTrue(numpy.array_equal(hypothesis.board, board))

if __name__ == '__main__':
    unittest.main()
