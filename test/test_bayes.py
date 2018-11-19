import unittest
import numpy as np
from eig.bayes import normalize, Bayes
from eig.battleship import EqualSizesDistribution, BattleshipHypothesisSpace


class TestBayes(unittest.TestCase):

    def test_normalize(self):
        self.assertTrue(np.array_equal(normalize(np.array([1])), np.array([1])))
        self.assertTrue(np.array_equal(normalize(np.array([1, 1])), np.array([.5, .5])))
        self.assertTrue(np.array_equal(normalize(np.array([1, 4])), np.array([.2, .8])))
        self.assertTrue(np.array_equal(normalize(np.array([0])), np.array([0])))
        self.assertTrue(np.array_equal(normalize(np.array([0, 0])), np.array([0, 0])))

    def test_uniform_prior(self):
        dummy_hypotheses = [None, None, None, None]
        belief = Bayes(dummy_hypotheses)
        self.assertTrue(np.array_equal(belief.belief, np.array([.25, .25, .25, .25])))

    def test_size_prior(self):
        hypotheses = BattleshipHypothesisSpace(grid_size=2, ship_labels=[1, 2], 
                ship_sizes=[1, 2], orientations=['V'])
        prior = EqualSizesDistribution(ship_labels=[1, 2])
        belief = Bayes(hypotheses, prior)
        for i, h in enumerate(hypotheses):
            h_sizes = [0, 0]
            for s in h.ships:
                h_sizes[s.ship_label - 1] = s.size
            h_sizes = tuple(h_sizes)
            if h_sizes == (1, 1):
                self.assertAlmostEqual(belief.belief[i], 1 / 48)
            elif h_sizes == (1, 2) or h_sizes == (2, 1):
                self.assertAlmostEqual(belief.belief[i], 1 / 16)
            elif h_sizes == (2, 2):
                self.assertAlmostEqual(belief.belief[i], 1 / 8)

    def test_update(self):
        dummy_hypotheses = [None, None, None, None, None]
        belief = Bayes(dummy_hypotheses)
        belief.update_belief([1, 2])
        self.assertTrue(np.array_equal(belief.belief, np.array([0, .5, .5, 0, 0])))
