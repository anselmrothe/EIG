import unittest
import numpy
from eig.battleship import Ship, BattleshipHypothesis

class TestHypothesis(unittest.TestCase):

    def test_hypothesis(self):
        ships = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='vertical'),
                 Ship(ship_label=2, topleft=(0, 1), size=2, orientation='horizontal')]
        hypothesis = BattleshipHypothesis(grid_size=3, ships=ships)
        
        board = numpy.array([1, 2, 2, 1, 0, 0, 1, 0, 0]).reshape(3, 3)
        self.assertTrue(numpy.array_equal(hypothesis.board, board))