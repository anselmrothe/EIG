import unittest
import numpy as np
from eig.battleship import Ship, \
    BattleshipHypothesis, BattleshipHypothesisSpace

class TestHypothesis(unittest.TestCase):

    def test_hypothesis(self):
        ships = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='V'),
                 Ship(ship_label=2, topleft=(0, 1), size=2, orientation='H')]
        hypothesis = BattleshipHypothesis(grid_size=3, ships=ships)
        
        board = np.array([1, 2, 2, 1, 0, 0, 1, 0, 0]).reshape(3, 3)
        self.assertTrue(np.array_equal(hypothesis.board, board))

    def test_invalid_hypothesis(self):
        ships = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='V'),
                 Ship(ship_label=2, topleft=(0, 1), size=3, orientation='H')]
        with self.assertRaises(ValueError):
            hypothesis = BattleshipHypothesis(grid_size=3, ships=ships)

    def test_hypothesis_space(self):
        hs = BattleshipHypothesisSpace(grid_size=3, ship_labels=[1, 2], 
                ship_sizes=[2, 3], orientations=['V'])
        self.assertEqual(len(hs), 54)

    def test_observation(self):
        hs = BattleshipHypothesisSpace(grid_size=3, ship_labels=[1, 2], 
                ship_sizes=[2], orientations=['V'])

        partly_revealed_board1 = np.array([[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]])
        self.assertEqual(len(hs.observe(partly_revealed_board1)), 24)

        partly_revealed_board2 = np.array([[-1, -1, -1], [-1, 1, -1], [-1, -1, 0]])
        self.assertEqual(len(hs.observe(partly_revealed_board2)), 6)

        partly_revealed_board3 = np.array([[0, 0, 0], [0, -1, 2], [0, -1, -1]])
        self.assertEqual(len(hs.observe(partly_revealed_board3)), 1)

        partly_revealed_board4 = np.array([[0, 0, 0], [0, 1, 2], [0, 0, -1]])
        self.assertEqual(len(hs.observe(partly_revealed_board4)), 0)

