import numpy
import unittest
from hypothesis import Hypothesis


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

    def test_create_hypothesis_space(self):
        create_hypothesis_space(grid_size=3, ships=[1, 2], shipsizes=[3])

if __name__ == '__main__':
    unittest.main()
