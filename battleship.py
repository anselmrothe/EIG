import numpy
import unittest
from hypothesis import Hypothesis


class BattleshipHypothesis(Hypothesis):

    def __init__(self, grid_size, ship_id, topleft, size, orientation):
        self.topleft = topleft
        self.size = size
        self.orientation = orientation
        board = numpy.zeros((grid_size, grid_size))
        board[topleft] = ship_id
        # TODO: based on orientation, fill in other locations
        self.board = board


class Test(unittest.TestCase):

    def test_hypothesis(self):
        hypothesis = BattleshipHypothesis(
            grid_size=3,
            ship_id=1, topleft=(1, 1), size=2, orientation='vertical')
        board = numpy.array([1, 0, 0, 1, 0, 0, 0, 0, 0]).reshape(3, 3)
        self.assertTrue(numpy.array_equal(hypothesis.board, board))

if __name__ == '__main__':
    unittest.main()
