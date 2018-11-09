import unittest
import numpy as np
from eig import Context, Bayes
from eig.battleship import BattleshipHypothesisSpace


class TestContext(unittest.TestCase):

    def test_observe(self):
        hs = BattleshipHypothesisSpace(grid_size=3, ship_labels=[1, 2], 
                ship_sizes=[2, 3], orientations=['V', 'H'])
        belief = Bayes(hs)
        observation = np.zeros((3, 3)) - 1
        observation[0, 0] = 0
        observation[1, 0] = observation[2, 0] = 1
        observation[1, 1] = 2
        
        context = Context(hs, belief)
        context.observe(observation)
        self.assertEqual(len(context.valid_ids), 4)

        observation[0, 1] = 2
        context.observe(observation)
        self.assertEqual(len(context.valid_ids), 2)

        observation[2, 1] = 3
        context.observe(observation)
        self.assertEqual(len(context.valid_ids), 0)
